import asyncio
import sys
sys.stdout.reconfigure(encoding='utf-8')
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import re

async def test_aliexpress_playwright(termino):
    print(f"\n--- Probando AliExpress con Playwright para: '{termino}' ---")
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled", "--no-sandbox"]
        )
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            locale="es-ES"
        )
        await context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        page = await context.new_page()
        url = f"https://es.aliexpress.com/w/wholesale-{termino.replace(' ', '-')}.html"
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)
        await page.wait_for_timeout(3000)
        
        print("AliExpress Page title:", await page.title())
        html = await page.content()
        soup = BeautifulSoup(html, "lxml")
        
        # Buscar enlaces de items /item/
        links = soup.find_all('a', href=True)
        item_links = [l for l in links if '/item/' in l['href']]
        print(f"Links de productos reales en AliExpress: {len(item_links)}")
        
        for l in item_links[:3]:
            # Extraer contenedor padre para buscar precio
            parent = l.find_parent('div')
            texto = l.text.strip()
            print("✔ PRODUCTO REAL:", texto[:70])
            href = l['href']
            if href.startswith('//'):
                href = 'https:' + href
            print("  LINK REAL:", href[:90])
        
        await browser.close()

asyncio.run(test_aliexpress_playwright("smartwatch"))
