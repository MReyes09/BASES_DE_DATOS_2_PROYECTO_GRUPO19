"""
Scraper para generar INSERTs de Evento_Falta.
Lee los HTMLs de partidos y extrae tarjetas (amarillas y rojas) para cada partido.

Tabla destino:
    Evento_Falta(Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, minuto_falta, entre_tiempo)

    - Tipo_Tarjeta: 1=AMARILLA, 2=ROJA
    - entre_tiempo: 1 si el minuto > 45 (segunda parte), 0 si <= 45
    - Se excluyen las "Otras tarjetas" (técnicos, asistentes, etc.)

Uso:
    python scraper_evento_falta.py
"""

import os
import re
import glob
from bs4 import BeautifulSoup

# =====================================================
# Configuración
# =====================================================
HTML_BASE = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..", "..",  # sube a BASES_DE_DATOS_2_PROYECTO_GRUPO19
    "Fase1", "data", "202300512", "01-html"
)
HTML_BASE = os.path.normpath(HTML_BASE)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "15evento_falta.sql")

# Regex para extraer minuto y tipo de tarjeta del texto de cada fila
# Formatos posibles:
#   "67' amarilla"
#   "90'+2' amarilla"
#   "35' expulsión - roja directa"
#   "90'+3' expulsión - roja por segunda amarilla"
TARJETA_RE = re.compile(
    r"(\d+)'(?:\+(\d+)')?\s+"
    r"(amarilla|expulsi[oó]n\s*-\s*roja\s+directa|expulsi[oó]n\s*-\s*roja\s+por\s+segunda\s+amarilla)",
    re.IGNORECASE
)


def parse_minuto(minuto_str, extra_str):
    """Construye el string de minuto, ej: '67' o '90+2'."""
    if extra_str:
        return f"{minuto_str}+{extra_str}"
    return minuto_str


def es_entre_tiempo(minuto_base):
    """Determina si la falta ocurrió en el segundo tiempo (minuto > 45)."""
    return 1 if int(minuto_base) > 45 else 0


def get_tipo_tarjeta_id(tipo_text):
    """Devuelve el Tipo_Tarjeta_id_ti_ta basado en el texto."""
    tipo_lower = tipo_text.lower().strip()
    if "roja" in tipo_lower:
        return 2  # ROJA
    return 1  # AMARILLA


def parse_tarjetas(filepath):
    """Extrae las tarjetas de un archivo HTML de partido.

    Retorna lista de dicts: {tipo_tarjeta_id, minuto, entre_tiempo, jugador}
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    # Buscar la sección de Tarjetas
    tarjetas_header = soup.find("h3", string=re.compile(r"Tarjetas", re.IGNORECASE))
    if not tarjetas_header:
        return []

    # La tabla de tarjetas es el siguiente sibling
    tarjetas_table = tarjetas_header.find_next("table")
    if not tarjetas_table:
        return []

    results = []
    en_otras_tarjetas = False

    rows = tarjetas_table.find_all("tr")
    for row in rows:
        # Detectar sección "Otras tarjetas" y dejar de procesar
        if row.find("strong", string=re.compile(r"Otras tarjetas", re.IGNORECASE)):
            en_otras_tarjetas = True
            continue

        if en_otras_tarjetas:
            continue

        # Saltar header
        if row.find("strong", string=re.compile(r"Selecci[oó]n|Tarjeta y Minutos", re.IGNORECASE)):
            continue

        tds = row.find_all("td")
        if len(tds) < 3:
            continue

        # td[1] = jugador, td[2] = tarjeta info
        jugador = tds[1].get_text(strip=True)
        tarjeta_text = tds[2].get_text(strip=True)

        if not jugador or not tarjeta_text:
            continue

        # Puede haber múltiples tarjetas en la misma celda (ej: amarilla + roja)
        for match in TARJETA_RE.finditer(tarjeta_text):
            minuto_base = match.group(1)
            extra = match.group(2)
            tipo_text = match.group(3)

            minuto_str = parse_minuto(minuto_base, extra)
            tipo_id = get_tipo_tarjeta_id(tipo_text)
            entre_t = es_entre_tiempo(minuto_base)

            results.append({
                "tipo_tarjeta_id": tipo_id,
                "minuto": minuto_str,
                "entre_tiempo": entre_t,
                "jugador": jugador,
            })

    return results


def main():
    print(f"Directorio HTML base: {HTML_BASE}")

    if not os.path.isdir(HTML_BASE):
        print(f"[ERROR] No existe el directorio: {HTML_BASE}")
        return

    year_dirs = sorted([
        d for d in os.listdir(HTML_BASE)
        if os.path.isdir(os.path.join(HTML_BASE, d)) and d.isdigit()
    ])

    print(f"Mundiales encontrados: {len(year_dirs)}")

    inserts = []
    inconsistencias = []
    ev_pa_counter = 0  # Contador correlativo del evento_partido (mismo orden que scraper_evento_partido.py)
    total_tarjetas = 0
    partidos_sin_tarjetas = 0

    for year_str in year_dirs:
        year_path = os.path.join(HTML_BASE, year_str)
        html_files = sorted(glob.glob(os.path.join(year_path, "*.html")))

        print(f"\n--- Mundial {year_str}: {len(html_files)} partidos ---")

        for html_file in html_files:
            ev_pa_counter += 1
            filename = os.path.basename(html_file)

            tarjetas = parse_tarjetas(html_file)

            if not tarjetas:
                partidos_sin_tarjetas += 1
                continue

            # PK = (Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta)
            # Solo se puede insertar UNA amarilla y UNA roja por partido.
            # Se toma la primera aparición de cada tipo; las extra se reportan.
            insertados = {}  # tipo_tarjeta_id -> primera tarjeta
            extras = []

            for t in tarjetas:
                tid = t["tipo_tarjeta_id"]
                if tid not in insertados:
                    insertados[tid] = t
                else:
                    extras.append(t)

            for tid, t in sorted(insertados.items()):
                insert = (
                    f"INSERT INTO Evento_Falta (Evento_Partido_id_ev_pa, Tipo_Tarjeta_id_ti_ta, "
                    f"minuto_falta, entre_tiempo) VALUES "
                    f"({ev_pa_counter}, {t['tipo_tarjeta_id']}, "
                    f"'{t['minuto']}', {t['entre_tiempo']});"
                )
                inserts.append((int(year_str), filename, insert))
                total_tarjetas += 1

            for t in extras:
                inconsistencias.append(
                    f"TARJETA EXTRA (omitida por PK) en {filename} (ev_pa={ev_pa_counter}): "
                    f"Tipo_Tarjeta={t['tipo_tarjeta_id']} jugador={t['jugador']}, "
                    f"minuto={t['minuto']}"
                )

    # Escribir archivo SQL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("-- =====================================================\n")
        f.write("-- Evento_Falta: Tarjetas de todos los mundiales\n")
        f.write("-- Generado automáticamente por scraper_evento_falta.py\n")
        f.write("-- =====================================================\n")
        f.write("-- Columnas:\n")
        f.write("--   Evento_Partido_id_ev_pa : FK a Evento_Partido\n")
        f.write("--   Tipo_Tarjeta_id_ti_ta   : FK a Tipo_Tarjeta (1=AMARILLA, 2=ROJA)\n")
        f.write("--   minuto_falta            : Minuto de la falta (ej: '67', '90+2')\n")
        f.write("--   entre_tiempo            : 1 si segundo tiempo, 0 si primer tiempo\n")
        f.write("-- =====================================================\n\n")

        current_year = None
        for year, filename, insert in inserts:
            if year != current_year:
                if current_year is not None:
                    f.write("\n")
                f.write(f"-- Mundial {year}\n")
                current_year = year
            f.write(f"{insert}\n")

        # Escribir inconsistencias al final del archivo
        if inconsistencias:
            f.write("\n\n-- =====================================================\n")
            f.write("-- INCONSISTENCIAS / MISMATCHING ENCONTRADOS\n")
            f.write("-- =====================================================\n")
            for inc in inconsistencias:
                f.write(f"-- {inc}\n")

    print(f"\n============================")
    print(f"Total tarjetas procesadas: {total_tarjetas}")
    print(f"Partidos sin tarjetas: {partidos_sin_tarjetas}")
    print(f"Inconsistencias: {len(inconsistencias)}")
    if inconsistencias:
        print("\nDetalle de inconsistencias:")
        for inc in inconsistencias:
            print(f"  - {inc.encode('ascii', 'replace').decode('ascii')}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
