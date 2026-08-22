# ============================================================
# scrapers/ebay.py — Scraper de eBay (scraping directo optimizado)
# ============================================================

import aiohttp
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper, Producto


class EbayScraper(BaseScraper):

    NOMBRE_TIENDA = "eBay"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    async def buscar(self, termino: str) -> list[Producto]:
        productos = []
        termino_encoded = termino.replace(" ", "+")
        url = f"https://www.ebay.com/sch/i.html?_nkw={termino_encoded}&_ipg={self.max_resultados * 2}"

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout, headers=self.HEADERS) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return []
                    html = await resp.text()

            soup = BeautifulSoup(html, "lxml")
            items = soup.select(".s-item__wrapper, li.s-item")

            for item in items:
                nombre_tag = item.select_one(".s-item__title")
                if not nombre_tag:
                    continue

                nombre_texto = nombre_tag.text.strip()
                if "shop on ebay" in nombre_texto.lower():
                    continue

                precio_tag = item.select_one(".s-item__price")
                envio_tag = item.select_one(".s-item__shipping, .s-item__logisticsCost")
                link_tag = item.select_one("a.s-item__link")

                if not precio_tag:
                    continue

                precio_texto = precio_tag.text.strip()
                if " to " in precio_texto:
                    precio_texto = precio_texto.split(" to ")[0]

                precio = self._limpiar_precio(precio_texto)
                url_producto = link_tag.get("href", "") if link_tag else ""

                # Costo de envío
                envio = 0.0
                if envio_tag:
                    texto_envio = envio_tag.text.strip().lower()
                    if "free" in texto_envio or "gratis" in texto_envio:
                        envio = 0.0
                    else:
                        envio = self._limpiar_precio(texto_envio)

                if precio > 0:
                    productos.append(
                        Producto(
                            tienda=self.NOMBRE_TIENDA,
                            nombre=self._truncar_nombre(nombre_texto),
                            precio=round(precio, 2),
                            envio=round(envio, 2),
                            total=round(precio + envio, 2),
                            url=url_producto,
                        )
                    )

                if len(productos) >= self.max_resultados:
                    break

        except Exception as e:
            print(f"  [eBay] Error: {e}")

        return productos
