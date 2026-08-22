# ============================================================
# app.py — Servidor Web Flask para PriceHunter (Shopify Scraper Real)
# ============================================================

import os
import sys
import asyncio
from flask import Flask, render_template, request, jsonify, send_file

# Forzar codificación UTF-8 en Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

from config import DIRECTORIO_OUTPUT
from scrapers.shopify_scraper import ShopifyScraper
from utils.exporter import exportar_a_excel, guardar_historial

app = Flask(__name__)
shopify_engine = ShopifyScraper()


@app.route("/")
def home():
    """Renderiza la aplicación web principal."""
    return render_template("index.html")


@app.route("/api/search")
def api_search():
    """Endpoint REST que ejecuta el scraping en tiempo real de tiendas Shopify."""
    termino = request.args.get("q", "").strip()

    if not termino:
        return jsonify({"error": "Parámetro de búsqueda requerido"}), 400

    # Ejecución concurrente en tiendas Shopify reales
    productos = asyncio.run(shopify_engine.buscar(termino, limite_por_tienda=4))

    # Generar Excel y guardar historial
    excel_url = None
    if productos:
        guardar_historial(termino, productos)
        ruta_excel = exportar_a_excel(termino, productos)
        nombre_excel = os.path.basename(ruta_excel)
        excel_url = f"/download/{nombre_excel}"

    return jsonify({
        "termino": termino,
        "total_encontrados": len(productos),
        "excel_url": excel_url,
        "productos": [p.to_dict() for p in productos],
    })


@app.route("/download/<path:filename>")
def download_excel(filename):
    """Descarga de reportes Excel generados."""
    file_path = os.path.join(DIRECTORIO_OUTPUT, filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    return jsonify({"error": "Archivo no encontrado"}), 404


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🚀 PriceHunter Shopify Real Scraper iniciado.")
    print("👉 Abre tu navegador en: http://127.0.0.1:5000")
    print("=" * 60 + "\n")
    app.run(host="127.0.0.1", port=5000, debug=False)
