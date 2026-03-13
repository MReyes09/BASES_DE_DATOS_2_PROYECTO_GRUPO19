"""
Descarga automática de HTMLs de losmundialesdefutbol.com usando Selenium.
Usa tu navegador Chrome real (hereda VPN, cookies, etc.)

USO:
  1. pip install selenium
  2. python download_htmls.py                     # descarga TODOS los paises
  3. python download_htmls.py argentina            # solo un pais
  4. python download_htmls.py argentina,brasil     # varios paises separados por coma

Los archivos se guardan en ./00-html/ como HTML puro (sin imagenes).
"""

import os
import re
import sys
import time
import random

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
except ImportError:
    print("❌ Selenium no esta instalado. Ejecuta:")
    print("   pip install selenium")
    sys.exit(1)

BASE_URL = "https://www.losmundialesdefutbol.com"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "00-html")
DELAY_MIN = 1.5
DELAY_MAX = 4.0
PAGE_TIMEOUT = 20


def create_driver():
    """Crea un driver de Chrome con configuracion humana."""
    opts = Options()
    # Mantener el navegador visible para que el usuario vea el progreso
    # opts.add_argument("--headless=new")  # Descomentar para modo invisible
    opts.add_argument("--disable-gpu")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--window-size=1280,900")
    opts.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    )
    # Desactivar el flag de Selenium/WebDriver
    opts.add_experimental_option("excludeSwitches", ["enable-automation"])
    opts.add_experimental_option("useAutomationExtension", False)

    driver = webdriver.Chrome(options=opts)
    driver.set_page_load_timeout(PAGE_TIMEOUT)

    # Ocultar la propiedad navigator.webdriver
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"},
    )
    return driver


def safe_filename(name):
    """Convierte un nombre a un nombre de archivo seguro."""
    return re.sub(r'[<>:"/\\|?*]', '_', name)


def wait_random():
    time.sleep(random.uniform(DELAY_MIN, DELAY_MAX))


def save_html(driver, filepath):
    """Guarda solo el HTML de la pagina actual."""
    html = driver.page_source
    with open(filepath, "w", encoding="utf-8") as f:
        # Agregar comentario con la URL original (formato estandar del navegador)
        url = driver.current_url
        f.write(f"<!-- saved from url=({len(url):04d}){url} -->\n")
        f.write(html)
    return filepath


def get_countries(driver):
    """Obtiene la lista de paises desde la pagina principal de jugadores."""
    url = f"{BASE_URL}/jugadores.php"
    print(f"🌍 Cargando pagina de paises: {url}")
    driver.get(url)
    wait_random()

    # Guardar el index de paises
    save_html(driver, os.path.join(OUTPUT_DIR, "_index_paises.html"))

    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="jugadores_indice/"]')
    countries = []
    seen = set()
    for link in links:
        href = link.get_attribute("href")
        match = re.search(r"jugadores_indice/(\w+)\.php", href)
        if match and match.group(1) not in seen:
            slug = match.group(1)
            seen.add(slug)
            name = link.text.strip() or slug
            countries.append({"slug": slug, "name": name})

    print(f"✅ {len(countries)} paises encontrados")
    return countries


def get_players_for_country(driver, country_slug):
    """Obtiene la lista de jugadores de un pais."""
    url = f"{BASE_URL}/jugadores_indice/{country_slug}.php"
    print(f"  📋 Cargando jugadores de {country_slug}: {url}")
    driver.get(url)
    wait_random()

    # Guardar el index del pais
    save_html(driver, os.path.join(OUTPUT_DIR, f"_index_{country_slug}.html"))

    # Buscar links a jugadores individuales
    links = driver.find_elements(By.CSS_SELECTOR, 'a[href*="/jugadores/"]')
    players = []
    seen = set()
    for link in links:
        href = link.get_attribute("href")
        match = re.search(r"/jugadores/(\w+)\.php", href)
        if match and match.group(1) not in seen:
            slug = match.group(1)
            seen.add(slug)
            name = link.text.strip() or slug
            players.append({"slug": slug, "name": name})

    return players


def download_player(driver, player_slug, country_slug):
    """Descarga el HTML de un jugador individual."""
    filepath = os.path.join(OUTPUT_DIR, f"{player_slug}.html")

    # Saltar si ya existe
    if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
        return "skip"

    url = f"{BASE_URL}/jugadores/{player_slug}.php"
    try:
        driver.get(url)
        wait_random()

        # Verificar que la pagina cargo correctamente
        if "403" in driver.title or "Forbidden" in driver.title:
            print(f"⚠️  403 para {player_slug}, esperando...")
            time.sleep(10)
            driver.get(url)
            wait_random()
            if "403" in driver.title or "Forbidden" in driver.title:
                return "403"

        save_html(driver, filepath)
        return "ok"

    except Exception as e:
        return f"error: {e}"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Archivo de progreso para poder resumir
    progress_file = os.path.join(OUTPUT_DIR, "_progress.txt")
    done_slugs = set()
    if os.path.exists(progress_file):
        with open(progress_file, "r") as f:
            done_slugs = set(line.strip() for line in f if line.strip())

    # Filtro de paises por argumento
    filter_countries = None
    if len(sys.argv) > 1:
        filter_countries = [c.strip().lower() for c in sys.argv[1].split(",")]

    driver = create_driver()
    total_downloaded = 0
    total_skipped = 0
    total_errors = 0

    try:
        countries = get_countries(driver)

        if filter_countries:
            countries = [c for c in countries if c["slug"].lower() in filter_countries]
            if not countries:
                print(f"❌ No se encontraron los paises: {filter_countries}")
                print("   Paises disponibles se guardaron en _index_paises.html")
                return

        for i_country, country in enumerate(countries, 1):
            print(f"\n🌍 [{i_country}/{len(countries)}] {country['name']} ({country['slug']})")

            players = get_players_for_country(driver, country["slug"])
            print(f"  📋 {len(players)} jugadores")

            for i_player, player in enumerate(players, 1):
                if player["slug"] in done_slugs:
                    total_skipped += 1
                    continue

                status = download_player(driver, player["slug"], country["slug"])

                if status == "ok":
                    total_downloaded += 1
                    done_slugs.add(player["slug"])
                    with open(progress_file, "a") as f:
                        f.write(player["slug"] + "\n")
                    print(f"  ✅ [{i_player}/{len(players)}] {player['name']}")
                elif status == "skip":
                    total_skipped += 1
                elif status == "403":
                    total_errors += 1
                    print(f"  ❌ [{i_player}/{len(players)}] {player['name']} - 403 persistente")
                else:
                    total_errors += 1
                    print(f"  ❌ [{i_player}/{len(players)}] {player['name']} - {status}")

            print(f"  📊 País completado: {country['name']}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Interrumpido por el usuario. El progreso esta guardado.")
    finally:
        driver.quit()

    print(f"\n🏁 RESULTADO FINAL:")
    print(f"   Descargados: {total_downloaded}")
    print(f"   Saltados (ya existian): {total_skipped}")
    print(f"   Errores: {total_errors}")
    print(f"   Archivos en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
