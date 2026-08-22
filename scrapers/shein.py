# ============================================================
# scrapers/shein.py — Scraper de Shein vía endpoints web
# ============================================================

import aiohttp
import re
from scrapers.base_scraper import BaseScraper, Producto


class SheinScraper(BaseScraper):

    NOMBRE_TIENDA = "Shein"

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    async def buscar(self, termino: str) -> list[Producto]:
        productos = []
        termino_encoded = termino.replace(" ", "-")
        url = f"https://us.shein.com/pdsearch/{termino_encoded}/"

        try:
            timeout = aiohttp.ClientTimeout(total=self.timeout)
            async with aiohttp.ClientSession(timeout=timeout, headers=self.HEADERS) as session:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        return []
                    html = await resp.text()

            # Extraer nombres y precios de los bloques de productos
            nombres = re.findall(r'goods_name":"([^"]+)"', html)
            precios = re.findall(r'salePrice":\{"amount":"?([0-9.]+)"?', html)

            for i in range(min(len(nombres), len(precios), self.max_resultados)):
                nombre = nombres[i].encode('utf-8').decode('unicode_escape', errors='ignore')
                precio = float(precios[i])

                if precio > 0:
                    productos.append(
                        Producto(
                            tienda=self.NOMBRE_TIENDA,
                            nombre=self._truncar_nombre(nombre),
                            precio=round(precio, 2),
                            envio=0.0,
                            total=round(precio, 2),
                            url="https://us.shein.com",
                        )
                    )

        except Exception as e:
            print(f"  [Shein] Error: {e}")

        return productos
