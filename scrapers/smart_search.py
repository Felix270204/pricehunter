# ============================================================
# scrapers/smart_search.py — Asistente Inteligente de Comparación Multi-Tienda
# ============================================================

import urllib.parse
from dataclasses import dataclass
from typing import Optional


@dataclass
class TiendaInfo:
    nombre: str
    badge_color: str
    logo_icon: str
    url_menor_precio: str
    url_mas_vendidos: str
    url_envio_gratis: str
    descripcion_filtro: str
    tiempo_estimado_envio: str
    moneda_predeterminada: str


def generar_enlaces_optimizados(termino: str) -> list[TiendaInfo]:
    """
    Construye URLs oficiales con parámetros de ordenamiento exactos
    para encontrar la oferta más económica en cada plataforma.
    """
    termino_query = urllib.parse.quote_plus(termino)
    termino_guion = termino.replace(" ", "-").lower()

    return [
        TiendaInfo(
            nombre="AliExpress",
            badge_color="bg-red-50 text-red-700 border-red-200",
            logo_icon="fa-brands fa-alipay",
            # sortType=price_asc (ordenar por menor precio)
            url_menor_precio=f"https://es.aliexpress.com/w/wholesale-{termino_guion}.html?sortType=price_asc",
            url_mas_vendidos=f"https://es.aliexpress.com/w/wholesale-{termino_guion}.html?sortType=total_tranpro_desc",
            url_envio_gratis=f"https://es.aliexpress.com/w/wholesale-{termino_guion}.html?isFreeShip=y&sortType=price_asc",
            descripcion_filtro="Filtro automático: Ordenado de menor a mayor precio + envío a tu país",
            tiempo_estimado_envio="10 - 20 días hábiles",
            moneda_predeterminada="USD",
        ),
        TiendaInfo(
            nombre="Shein",
            badge_color="bg-pink-50 text-pink-700 border-pink-200",
            logo_icon="fa-solid fa-bag-shopping",
            # sort=2 (precio ascendente en Shein)
            url_menor_precio=f"https://us.shein.com/pdsearch/{termino_query}/?sort=2",
            url_mas_vendidos=f"https://us.shein.com/pdsearch/{termino_query}/?sort=4",
            url_envio_gratis=f"https://us.shein.com/pdsearch/{termino_query}/?sort=2",
            descripcion_filtro="Filtro automático: Menor precio disponible en catálogo Shein US/Global",
            tiempo_estimado_envio="7 - 15 días hábiles",
            moneda_predeterminada="USD",
        ),
        TiendaInfo(
            nombre="Amazon",
            badge_color="bg-amber-50 text-amber-800 border-amber-200",
            logo_icon="fa-brands fa-amazon",
            # s=price-asc-rank (ordenar por precio ascendente en Amazon)
            url_menor_precio=f"https://www.amazon.com/s?k={termino_query}&s=price-asc-rank",
            url_mas_vendidos=f"https://www.amazon.com/s?k={termino_query}&s=exact-aware-popularity-rank",
            url_envio_gratis=f"https://www.amazon.com/s?k={termino_query}&s=price-asc-rank&rh=p_76%3A2661625011",
            descripcion_filtro="Filtro automático: Ordenado por precio más bajo + Prime / Global Shipping",
            tiempo_estimado_envio="3 - 7 días hábiles",
            moneda_predeterminada="USD",
        ),
        TiendaInfo(
            nombre="eBay",
            badge_color="bg-blue-50 text-blue-700 border-blue-200",
            logo_icon="fa-brands fa-ebay",
            # _sop=15 (precio + envío más bajo en eBay)
            url_menor_precio=f"https://www.ebay.com/sch/i.html?_nkw={termino_query}&_sop=15",
            url_mas_vendidos=f"https://www.ebay.com/sch/i.html?_nkw={termino_query}&_sop=12",
            url_envio_gratis=f"https://www.ebay.com/sch/i.html?_nkw={termino_query}&_sop=15&LH_FS=1",
            descripcion_filtro="Filtro automático: Precio + Envío más bajo verificado en eBay Global",
            tiempo_estimado_envio="5 - 15 días hábiles",
            moneda_predeterminada="USD",
        ),
        TiendaInfo(
            nombre="MercadoLibre",
            badge_color="bg-yellow-50 text-yellow-800 border-yellow-200",
            logo_icon="fa-solid fa-handshake",
            # _OrderId_PRICE_ASC (ordenar de menor a mayor precio)
            url_menor_precio=f"https://listado.mercadolibre.com.mx/{termino_guion}_OrderId_PRICE_ASC",
            url_mas_vendidos=f"https://listado.mercadolibre.com.mx/{termino_guion}",
            url_envio_gratis=f"https://listado.mercadolibre.com.mx/{termino_guion}_OrderId_PRICE_ASC_Envio_Gratis",
            descripcion_filtro="Filtro automático: Ordenado de menor a mayor precio regional + Envío Full",
            tiempo_estimado_envio="1 - 4 días hábiles",
            moneda_predeterminada="MXN / USD",
        ),
    ]
