from scrapers.base_scraper import BaseScraper, Producto
from scrapers.shopping_aggregator import ShoppingAggregatorScraper
from scrapers.mercadolibre import MercadoLibreScraper
from scrapers.ebay import EbayScraper
from scrapers.aliexpress import AliExpressScraper
from scrapers.amazon import AmazonScraper
from scrapers.shein import SheinScraper

__all__ = [
    "BaseScraper",
    "Producto",
    "ShoppingAggregatorScraper",
    "MercadoLibreScraper",
    "EbayScraper",
    "AliExpressScraper",
    "AmazonScraper",
    "SheinScraper",
]
