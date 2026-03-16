"""
Scraper para generar INSERTs de Partido_Plantilla (tabla intermedia).
Recorre los HTMLs en el mismo orden que scraper_evento_partido.py
y extrae las 2 plantillas (pais, entrenador) de cada partido.

Tabla destino:
    Partido_Plantilla(Plantilla_id_pla, Evento_Partido_id_ev_pa)

Uso:
    python scraper_partido_plantilla.py
"""

import os
import re
import glob
from pathlib import Path
from bs4 import BeautifulSoup

# =====================================================
# Configuración
# =====================================================
BASE_DIR = Path(__file__).resolve().parent

HTML_BASE = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..", "..",  # sube a BASES_DE_DATOS_2_PROYECTO_GRUPO19
    "Fase1", "data", "202300512", "01-html"
)
HTML_BASE = os.path.normpath(HTML_BASE)

PLANTILLA_SQL = BASE_DIR.parent / "10-plantilla" / "10plantilla.sql"
PAIS_SQL = Path(
    r"c:\Users\danie.000\Documents\BD2\Projecto1\BASES_DE_DATOS_2_PROYECTO_GRUPO19"
    r"\Fase1_v2\load_data\data\Nivel1\05-pais\5pais.sql"
)

OUTPUT_FILE = BASE_DIR / "17partido_plantilla.sql"

# Mapeo de nombres HTML -> nombres SQL (mismo que scraper_plantilla.py)
PAIS_ALIAS = {
    "Emiratos Arabes": "Emiratos Árabes Unidos",
    "Paises Bajos": "Países Bajos",
    "Iraq": "Irak",
    "Indias Orientales Holand.": "Indonesia",
    "RF de Yugoslavia": "Yugoslavia",
    "Serbia y Montenegro": "Serbia",
}


def cargar_paises():
    """Carga el mapeo nombre_pais -> id_pais desde el SQL de paises."""
    mapa = {}
    pattern = re.compile(r"VALUES\s*\(\s*(\d+),\s*'([^']*(?:''[^']*)*)'", re.I)

    with open(PAIS_SQL, encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if "INSERT INTO Pais" not in linea:
                continue
            m = pattern.search(linea)
            if m:
                id_pa = int(m.group(1))
                nombre = m.group(2).replace("''", "'")
                if nombre not in mapa:
                    mapa[nombre] = id_pa

    print(f"{len(mapa)} paises cargados desde SQL")
    return mapa


def buscar_pais_id(nombre_html, paises):
    """Busca el id del pais, usando alias si es necesario."""
    nombre = PAIS_ALIAS.get(nombre_html, nombre_html)

    if nombre in paises:
        return paises[nombre]

    # Busqueda sin acentos como fallback
    def sin_acentos(s):
        return (s.replace('á', 'a').replace('é', 'e').replace('í', 'i')
                 .replace('ó', 'o').replace('ú', 'u').replace('ñ', 'n')
                 .replace('Á', 'A').replace('É', 'E').replace('Í', 'I')
                 .replace('Ó', 'O').replace('Ú', 'U').replace('Ñ', 'N'))

    nombre_norm = sin_acentos(nombre).lower()
    for nombre_sql, id_pa in paises.items():
        if sin_acentos(nombre_sql).lower() == nombre_norm:
            return id_pa

    return None


def cargar_plantillas():
    """Carga el mapeo (pais_id, entrenador) -> id_pla desde 10plantilla.sql."""
    mapa = {}
    pattern = re.compile(
        r"VALUES\s*\(\s*(\d+),\s*(\d+),\s*'([^']*(?:''[^']*)*)'",
        re.I
    )

    with open(PLANTILLA_SQL, encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if "INSERT INTO Plantilla" not in linea:
                continue
            m = pattern.search(linea)
            if m:
                id_pla = int(m.group(1))
                pais_id = int(m.group(2))
                entrenador = m.group(3).replace("''", "'")
                mapa[(pais_id, entrenador)] = id_pla

    print(f"{len(mapa)} plantillas cargadas desde SQL")
    return mapa


def extraer_plantillas_de_html(filepath, paises):
    """Extrae pares (pais_id, entrenador) de un HTML de partido."""
    resultados = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Buscar la seccion de Jugadores
    h3 = soup.find("h3", string=re.compile(r"Jugadores", re.I))
    if not h3:
        return resultados

    # El contenedor padre con las 2 tablas de equipos
    container = h3.find_next("div", class_="clearfix")
    if not container:
        return resultados

    # Cada equipo esta en una tabla class="a-center"
    tablas = container.find_all("table", class_="a-center")

    for tabla in tablas:
        pais_html = None
        entrenador = None

        # Buscar pais: td con height:40px que contiene img con alt
        td_pais = tabla.find("td", style=re.compile(r"height:\s*40px"))
        if td_pais:
            img = td_pais.find("img", alt=True)
            if img:
                pais_html = img["alt"].strip()

        # Buscar entrenador
        for td in tabla.find_all("td"):
            strong = td.find("strong")
            if strong and "Entrenador:" in strong.get_text():
                texto = td.get_text()
                entrenador = texto.split("Entrenador:")[-1].strip()
                break

        if pais_html and entrenador:
            pais_id = buscar_pais_id(pais_html, paises)
            if pais_id is not None:
                resultados.append((pais_id, entrenador))
            else:
                print(f"  [WARN] Pais no encontrado: '{pais_html}' en {filepath}")

    return resultados


def main():
    print("SCRAPER PARTIDO_PLANTILLA - Tabla intermedia")
    print("=" * 60)

    if not os.path.isdir(HTML_BASE):
        print(f"[ERROR] No existe el directorio: {HTML_BASE}")
        return

    paises = cargar_paises()
    plantillas = cargar_plantillas()

    # Obtener directorios de años (mismo orden que scraper_evento_partido.py)
    year_dirs = sorted([
        d for d in os.listdir(HTML_BASE)
        if os.path.isdir(os.path.join(HTML_BASE, d)) and d.isdigit()
    ])

    print(f"Mundiales encontrados: {len(year_dirs)}")

    inserts = []
    id_ev_pa = 1  # Mismo contador que scraper_evento_partido.py
    sin_match = 0
    total_relaciones = 0

    for year_str in year_dirs:
        year_path = os.path.join(HTML_BASE, year_str)
        html_files = sorted(glob.glob(os.path.join(year_path, "*.html")))

        year_count = 0

        for html_file in html_files:
            # Extraer las plantillas (pais_id, entrenador) del partido
            pares = extraer_plantillas_de_html(html_file, paises)

            for pais_id, entrenador in pares:
                clave = (pais_id, entrenador)
                id_pla = plantillas.get(clave)

                if id_pla is None:
                    print(f"  [WARN] Plantilla no encontrada: pais_id={pais_id}, "
                          f"entrenador='{entrenador}' en {os.path.basename(html_file)}")
                    sin_match += 1
                    continue

                inserts.append((int(year_str), id_pla, id_ev_pa))
                year_count += 1
                total_relaciones += 1

            id_ev_pa += 1

        print(f"  Mundial {year_str}: {year_count} relaciones")

    # Escribir archivo SQL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("-- =====================================================\n")
        f.write("-- Partido_Plantilla: Relación Partidos <-> Plantillas\n")
        f.write("-- Generado automáticamente por scraper_partido_plantilla.py\n")
        f.write("-- =====================================================\n")
        f.write("-- Columnas:\n")
        f.write("--   Plantilla_id_pla        : FK a Plantilla (id_pla)\n")
        f.write("--   Evento_Partido_id_ev_pa : FK a Evento_Partido (id_ev_pa)\n")
        f.write(f"-- Total: {total_relaciones} registros\n")
        f.write("-- =====================================================\n\n")

        current_year = None
        for year, id_pla, ev_pa_id in inserts:
            if year != current_year:
                if current_year is not None:
                    f.write("\n")
                f.write(f"-- Mundial {year}\n")
                current_year = year
            f.write(
                f"INSERT INTO Partido_Plantilla (Plantilla_id_pla, "
                f"Evento_Partido_id_ev_pa) VALUES ({id_pla}, {ev_pa_id});\n"
            )

    print(f"\n{'=' * 60}")
    print(f"Total relaciones generadas: {total_relaciones}")
    print(f"Sin match (plantillas no encontradas): {sin_match}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
