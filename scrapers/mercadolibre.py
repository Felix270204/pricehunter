# ============================================================
# scrapers/mercadolibre.py — Scraper de MercadoLibre vía HTML directo
# ============================================================

import aiohttp
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper, Producto


class MercadoLibreScraper(BaseScraper):

    NOMBRE_TIENDA = "MercadoLibre"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    async def buscar(self, termino: str) -> list[Producto]:
        productos = []
        termino_encoded = termino.replace(" ", "-").lower()
        # Usamos la búsqueda de MercadoLibre México (precios en MXN convertidos a USD aprox ~18 MXN/USD)
        url = f"https://listado.mercadolibre.com.mx/{termino_encoded}"

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout, headers=self.HEADERS) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return []
                    html = await resp.text()

            soup = BeautifulSoup(html, "lxml")
            items = soup.select(".ui-search-result__wrapper, .poly-card, .ui-search-layout__item")

            for item in items[:self.max_resultados]:
                try:
                    nombre_tag = item.select_one(".poly-component__title, .ui-search-item__title")
                    precio_entero = item.select_one(".andes-money-amount__fraction")
                    link_tag = item.select_one("a.poly-component__title, a.ui-search-link, a")

                    if not nombre_tag or not precio_entero:
                        continue

                    nombre = self._truncar_nombre(nombre_tag.text.strip())
                    precio_mxn = self._limpiar_precio(precio_entero.text)
                    precio_usd = round(precio_mxn / 18.0, 2)  # Tasa representativa MXN a USD

                    # Envío gratis
                    envio_tag = item.select_one(".poly-component__shipping, .ui-search-item__shipping--free")
                    envio = 0.0 if (envio_tag and "gratis" in envio_tag.text.lower()) else 4.50

                    url_p = link_tag.get("href", "") if link_tag else ""

                    if precio_usd > 0:
                        productos.append(
                            Producto(
                                tienda=self.NOMBRE_TIENDA,
                                nombre=nombre,
                                precio=precio_usd,
                                envio=envio,
                                total=round(precio_usd + envio, 2),
                                url=url_p,
                            )
                        )
                except Exception:
                    continue

        except Exception as e:
            print(f"  [MercadoLibre] Error: {e}")

        return productos
