# ============================================================
# scrapers/aliexpress.py — Scraper de AliExpress con búsqueda directa
# ============================================================

import aiohttp
import re
import json
from bs4 import BeautifulSoup
from scrapers.base_scraper import BaseScraper, Producto


class AliExpressScraper(BaseScraper):

    NOMBRE_TIENDA = "AliExpress"

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
        url = f"https://www.aliexpress.com/wholesale?SearchText={termino_encoded}"

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout, headers=self.HEADERS) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return []
                    html = await resp.text()

            # Buscar patrones de precios y títulos en los datos JSON embebidos
            matches_title = re.findall(r'"title":\s*\{"displayTitle":\s*"([^"]+)"', html)
            matches_price = re.findall(r'"minPrice":\s*([0-9.]+)', html)

            for i in range(min(len(matches_title), len(matches_price), self.max_resultados)):
                titulo = matches_title[i]
                precio = float(matches_price[i])
                envio = 0.0  # AliExpress frecuentemente incluye envío gratis o muy económico

                if precio > 0:
                    productos.append(
                        Producto(
                            tienda=self.NOMBRE_TIENDA,
                            nombre=self._truncar_nombre(titulo),
                            precio=round(precio, 2),
                            envio=round(envio, 2),
                            total=round(precio + envio, 2),
                            url="https://www.aliexpress.com",
                        )
                    )

        except Exception as e:
            print(f"  [AliExpress] Error: {e}")

        return productos
