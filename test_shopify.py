import requests
import sys
sys.stdout.reconfigure(encoding='utf-8')

tiendas = [
    ("Spigen", "www.spigen.com"),
    ("Allbirds", "www.allbirds.com"),
    ("UNTUCKit", "untuckit.com"),
    ("ColourPop", "colourpop.com"),
    ("Alo Yoga", "aloyoga.com"),
]

for t_nombre, d in tiendas:
    url = f"https://{d}/search/suggest.json?q=shirt&resources[type]=product"
    try:
        r = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        data = r.json()
        prods = data.get("resources", {}).get("results", {}).get("products", [])
        print(f"[{t_nombre}] Encontrados para 'shirt': {len(prods)}")
        for p in prods[:2]:
            print(f"  Titulo: {p.get('title')}")
            print(f"  Precio: ${p.get('price')}")
            print(f"  Link: https://{d}{p.get('url')}\n")
    except Exception as e:
        print(f"[{t_nombre}] Error: {e}")
