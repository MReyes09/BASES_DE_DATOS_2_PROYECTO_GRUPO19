#!/usr/bin/env python3

import os
import re
from pathlib import Path
from bs4 import BeautifulSoup

HTML_DIR = Path(r"c:\Users\danie.000\Documents\BD2\Projecto1\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1\data\202300512\01-html")
PAIS_SQL = Path(r"c:\Users\danie.000\Documents\BD2\Projecto1\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\5pais.sql")
OUTPUT_SQL = Path(__file__).parent / "10plantilla.sql"

# Mapeo de nombres HTML -> nombres SQL (para los que difieren)
PAIS_ALIAS = {
    "Emiratos Arabes": "Emiratos Árabes Unidos",
    "Paises Bajos": "Países Bajos",
    "Iraq": "Irak",
    "Indias Orientales Holand.": "Indonesia",
    "RF de Yugoslavia": "Yugoslavia",
    "Serbia y Montenegro": "Serbia",
}


def cargar_paises():
    """Carga el mapeo nombre_pais -> id_pais desde el SQL."""
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


def extraer_plantillas_de_html(filepath):
    """Extrae pares (pais, entrenador) de un HTML de partido."""
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
        pais = None
        entrenador = None

        # Buscar pais: td con height:40px que contiene img con alt
        td_pais = tabla.find("td", style=re.compile(r"height:\s*40px"))
        if td_pais:
            img = td_pais.find("img", alt=True)
            if img:
                pais = img["alt"].strip()

        # Buscar entrenador
        for td in tabla.find_all("td"):
            strong = td.find("strong")
            if strong and "Entrenador:" in strong.get_text():
                texto = td.get_text()
                entrenador = texto.split("Entrenador:")[-1].strip()
                break

        if pais and entrenador:
            resultados.append((pais, entrenador))

    return resultados


def main():
    print("SCRAPER PLANTILLA - Entrenadores por pais")
    print("=" * 60)

    paises = cargar_paises()

    # Recopilar todas las plantillas unicas (pais, entrenador)
    plantillas_unicas = set()
    sin_match = set()

    year_dirs = sorted([
        d for d in HTML_DIR.iterdir()
        if d.is_dir() and d.name.isdigit()
    ])

    total_html = 0
    for year_dir in year_dirs:
        html_files = list(year_dir.glob("*.html"))
        total_html += len(html_files)

        for html_file in html_files:
            pares = extraer_plantillas_de_html(html_file)
            for pais_html, entrenador in pares:
                pais_id = buscar_pais_id(pais_html, paises)
                if pais_id is None:
                    sin_match.add(pais_html)
                    continue
                plantillas_unicas.add((pais_id, entrenador))

    print(f"{total_html} archivos HTML procesados")
    print(f"{len(plantillas_unicas)} plantillas unicas encontradas")

    if sin_match:
        print(f"\nPaises sin match ({len(sin_match)}):")
        for p in sorted(sin_match):
            print(f"  - {p}")

    # Ordenar por pais_id y luego por nombre del entrenador
    plantillas = sorted(plantillas_unicas, key=lambda x: (x[0], x[1]))

    # Generar SQL
    with open(OUTPUT_SQL, 'w', encoding='utf-8') as f:
        f.write("-- INSERTs para tabla Plantilla\n")
        f.write(f"-- Total: {len(plantillas)} registros\n\n")

        for i, (pais_id, entrenador) in enumerate(plantillas, 1):
            entrenador_escaped = entrenador.replace("'", "''")
            f.write(
                f"INSERT INTO Plantilla (id_pla, Pais_id_pa, director_tecnico_pla) "
                f"VALUES ({i}, {pais_id}, '{entrenador_escaped}');\n"
            )

    print(f"\nSQL guardado en: {OUTPUT_SQL}")
    print(f"Total INSERTs: {len(plantillas)}")


if __name__ == "__main__":
    main()
