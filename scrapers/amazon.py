# ============================================================
# scrapers/amazon.py — Scraper de Amazon con Playwright (stealth)
# ============================================================

from scrapers.base_scraper import BaseScraper, Producto


class AmazonScraper(BaseScraper):

    NOMBRE_TIENDA = "Amazon"

    async def buscar(self, termino: str) -> list[Producto]:
        productos = []
        try:
            from playwright.async_api import async_playwright

            termino_encoded = termino.replace(" ", "+")
            url = f"https://www.amazon.com/s?k={termino_encoded}"

            async with async_playwright() as p:
                browser = await p.chromium.launch(
                    headless=True,
                    args=[
                        "--no-sandbox",
                        "--disable-blink-features=AutomationControlled",
                    ]
                )
                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    ),
                    viewport={"width": 1280, "height": 800},
                    locale="en-US",
                )

                # Ocultar que es un navegador automatizado
                await context.add_init_script("""
                    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
                """)

                page = await context.new_page()

                await page.goto(url, timeout=self.timeout * 1000, wait_until="domcontentloaded")
                await page.wait_for_timeout(2000)

                # Verificar si Amazon redirigió a CAPTCHA
                if "captcha" in page.url.lower() or "robot" in (await page.title()).lower():
                    print("  [Amazon] ⚠️  Bloqueado por CAPTCHA — omitiendo Amazon")
                    await browser.close()
                    return []

                items = await page.query_selector_all("div[data-component-type='s-search-result']")

                for item in items[:self.max_resultados]:
                    try:
                        nombre_el = await item.query_selector("h2 span")
                        precio_entero_el = await item.query_selector(".a-price-whole")
                        precio_frac_el = await item.query_selector(".a-price-fraction")
                        link_el = await item.query_selector("h2 a")
                        envio_el = await item.query_selector(".a-color-secondary .a-text-bold")

                        if not nombre_el or not precio_entero_el:
                            continue

                        nombre = await nombre_el.inner_text()
                        precio_str = await precio_entero_el.inner_text()
                        frac_str = await precio_frac_el.inner_text() if precio_frac_el else "00"
                        precio_str = precio_str.replace(",", "").strip().rstrip(".")
                        precio = float(f"{precio_str}.{frac_str.strip()}")

                        link_href = await link_el.get_attribute("href") if link_el else ""
                        url_producto = f"https://www.amazon.com{link_href}" if link_href.startswith("/") else link_href

                        # Costo de envío
                        envio = 0.0
                        if envio_el:
                            envio_texto = (await envio_el.inner_text()).lower()
                            if "free" not in envio_texto:
                                envio = self._limpiar_precio(envio_texto)

                        if precio > 0:
                            productos.append(Producto(
                                tienda=self.NOMBRE_TIENDA,
                                nombre=self._truncar_nombre(nombre.strip()),
                                precio=round(precio, 2),
                                envio=round(envio, 2),
                                total=round(precio + envio, 2),
                                url=url_producto,
                            ))
                    except Exception:
                        continue

                await browser.close()

        except Exception as e:
            print(f"  [Amazon] Error: {e}")

        return productos
