import sys
sys.stdout.reconfigure(encoding='utf-8')
from curl_cffi import requests
from bs4 import BeautifulSoup
import re
import urllib.parse

def test_aliexpress_real(query):
    # Endpoint de búsqueda directa con headers emulados
    url = f"https://www.aliexpress.com/wholesale?SearchText={urllib.parse.quote_plus(query)}"
    r = requests.get(url, impersonate="chrome120")
    print("AliExpress HTML status:", r.status_code, "Len:", len(r.text))
    # Buscar patrones de items reales
    items = re.findall(r'\"productId\":\"?([0-9]+)\"?.*?\"minPrice\":([0-9.]+).*?\"displayTitle\":\"([^\"]+)\"', r.text)
    print("AliExpress items encontrados por regex:", len(items))
    for it in items[:2]:
        print(" -> Id:", it[0], "Precio:", it[1], "Titulo:", it[2][:50])

test_aliexpress_real("ps5 slim")
