"""
Scraper para generar INSERTs de Evento_Partido.
Lee los HTMLs de partidos y extrae fecha + fase para cada mundial.

Tabla destino:
    Evento_Partido(id_ev_pa, fecha_ev_pa, Llave_Mundial_id_mu, Llave_Mundial_id_fa)

Uso:
    python scraper_evento_partido.py
"""

import os
import re
import glob

# =====================================================
# Configuración
# =====================================================
HTML_BASE = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..", "..",  # sube a BASES_DE_DATOS_2_PROYECTO_GRUPO19
    "Fase1", "data", "202300512", "01-html"
)
HTML_BASE = os.path.normpath(HTML_BASE)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "12evento_partido.sql")

# Mapeo año -> Mundial_id_mu (de 4mundial.sql)
YEAR_TO_MUNDIAL = {
    2026: 1,  2022: 2,  2018: 3,  2014: 4,  2010: 5,
    2006: 6,  2002: 7,  1998: 8,  1994: 9,  1990: 10,
    1986: 11, 1982: 12, 1978: 13, 1974: 14, 1970: 15,
    1966: 16, 1962: 17, 1958: 18, 1954: 19, 1950: 20,
    1938: 21, 1934: 22, 1930: 23,
}

# Mapeo fase HTML -> Fase_id_fa (de 1fase.sql)
# 1=Dieciseisavos, 2=Octavos, 3=Cuartos, 4=Semifinales, 5=Final
FASE_MAP = {
    "Final": 5,
    "Tercer Puesto": 5,
    "Ronda Final": 5,
    "Semifinales": 4,
    "Cuartos de Final": 3,
    "Octavos de Final": 2,
}
# Fases que empiezan con "1ra Ronda" -> 1 (Dieciseisavos)
# Fases que empiezan con "2da Ronda" -> 2 (Octavos)

# Meses en español
MESES = {
    "Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4,
    "Mayo": 5, "Junio": 6, "Julio": 7, "Agosto": 8,
    "Septiembre": 9, "Octubre": 10, "Noviembre": 11, "Diciembre": 12,
}

# Regex para extraer fase del HTML
FASE_RE = re.compile(
    r'<a\s+href="\.\./mundiales/\d{4}_[^"]+\.php">([^<]+)</a>\s*</span>\s*</p>',
    re.IGNORECASE
)

# Regex para extraer fecha del HTML
FECHA_RE = re.compile(
    r'Fecha:\s*\w+\s+(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})',
    re.IGNORECASE
)


def get_fase_id(fase_text):
    """Mapea el texto de fase del HTML al Fase_id_fa."""
    fase_text = fase_text.strip()
    if fase_text in FASE_MAP:
        return FASE_MAP[fase_text]
    if fase_text.startswith("1ra Ronda"):
        return 1  # Dieciseisavos
    if fase_text.startswith("2da Ronda"):
        return 2  # Octavos
    print(f"  [WARN] Fase no reconocida: '{fase_text}'")
    return None


def parse_html(filepath):
    """Extrae (fecha_str, fase_id) de un archivo HTML."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extraer fase
    fase_match = FASE_RE.search(content)
    if not fase_match:
        print(f"  [ERROR] No se encontró fase en: {filepath}")
        return None
    fase_text = fase_match.group(1).strip()
    fase_id = get_fase_id(fase_text)
    if fase_id is None:
        return None

    # Extraer fecha
    fecha_match = FECHA_RE.search(content)
    if not fecha_match:
        print(f"  [ERROR] No se encontró fecha en: {filepath}")
        return None

    day = int(fecha_match.group(1))
    month_name = fecha_match.group(2)
    year = int(fecha_match.group(3))

    month = MESES.get(month_name)
    if month is None:
        print(f"  [ERROR] Mes no reconocido: '{month_name}' en {filepath}")
        return None

    # Formato Oracle DATE: DD/MM/YYYY
    fecha_str = f"{day:02d}/{month:02d}/{year}"

    return fecha_str, fase_id


def main():
    print(f"Directorio HTML base: {HTML_BASE}")

    if not os.path.isdir(HTML_BASE):
        print(f"[ERROR] No existe el directorio: {HTML_BASE}")
        return

    # Obtener todos los directorios de años (solo numéricos)
    year_dirs = sorted([
        d for d in os.listdir(HTML_BASE)
        if os.path.isdir(os.path.join(HTML_BASE, d)) and d.isdigit()
    ])

    print(f"Mundiales encontrados: {len(year_dirs)}")

    inserts = []
    id_counter = 1
    errors = 0

    for year_str in year_dirs:
        year = int(year_str)
        mundial_id = YEAR_TO_MUNDIAL.get(year)
        if mundial_id is None:
            print(f"  [SKIP] Año {year} no tiene Mundial_id asignado")
            continue

        year_path = os.path.join(HTML_BASE, year_str)
        html_files = sorted(glob.glob(os.path.join(year_path, "*.html")))

        print(f"\n--- Mundial {year} (id={mundial_id}): {len(html_files)} partidos ---")

        for html_file in html_files:
            result = parse_html(html_file)
            if result is None:
                errors += 1
                continue

            fecha_str, fase_id = result
            filename = os.path.basename(html_file)

            insert = (
                f"INSERT INTO Evento_Partido (id_ev_pa, fecha_ev_pa, "
                f"Llave_Mundial_id_mu, Llave_Mundial_id_fa) VALUES "
                f"({id_counter}, TO_DATE('{fecha_str}', 'DD/MM/YYYY'), "
                f"{mundial_id}, {fase_id});"
            )
            inserts.append((year, filename, insert))
            id_counter += 1

    # Escribir archivo SQL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("-- =====================================================\n")
        f.write("-- Evento_Partido: Partidos de todos los mundiales\n")
        f.write("-- Generado automáticamente por scraper_evento_partido.py\n")
        f.write("-- =====================================================\n")
        f.write("-- Columnas:\n")
        f.write("--   id_ev_pa            : ID autoincremental del partido\n")
        f.write("--   fecha_ev_pa         : Fecha del partido\n")
        f.write("--   Llave_Mundial_id_mu : FK a Mundial (Mundial_id_mu)\n")
        f.write("--   Llave_Mundial_id_fa : FK a Fase (Fase_id_fa)\n")
        f.write("-- =====================================================\n\n")

        current_year = None
        for year, filename, insert in inserts:
            if year != current_year:
                if current_year is not None:
                    f.write("\n")
                f.write(f"-- Mundial {year}\n")
                current_year = year
            f.write(f"{insert}\n")

    total = id_counter - 1
    print(f"\n============================")
    print(f"Total partidos procesados: {total}")
    print(f"Errores: {errors}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
