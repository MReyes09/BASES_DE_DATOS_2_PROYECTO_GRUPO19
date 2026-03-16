"""
Scraper para generar INSERTs de Evento_Gol.
Lee los HTMLs de partidos y extrae goles para cada partido.

Tabla destino:
    Evento_Gol(id_ev_go, Evento_Partido_id_ev_pa, Jugador_id_ju, tiempo_gol,
               entre_tiempo_ev_go, penal)

    - id_ev_go            : ID autoincremental
    - Evento_Partido_id_ev_pa : FK a Evento_Partido
    - Jugador_id_ju       : FK a Jugador
    - tiempo_gol          : Minuto del gol (ej: '23', '90+2')
    - entre_tiempo_ev_go  : '1' si segundo tiempo (minuto > 45), '0' si primero
    - penal               : 1 si fue de penal, 0 si no

Uso:
    python scraper_evento_gol.py
"""

import os
import re
import glob
import unicodedata
from bs4 import BeautifulSoup

# =====================================================
# Mapeo de alias: nombre HTML → nombre EXACTO en 3jugador.sql
# =====================================================
ALIAS_JUGADORES = {
    # Apodos / nombres cortos → nombre legal completo
    "pele": "edson arantes do nascimento",
    "garrincha": "manuel francisco dos santos",
    "bobby charlton": "sir robert charlton",
    "ronaldinho": "ronaldo de assis moreira",
    "kaka": "ricardo izecson dos santos leite",
    "xabi alonso": "xabier alonso olano",
    "edinson cavani": "edinson roberto cavani gomez",
    "romelu lukaku": "romelu menama lukaku bolingoli",
    "marcelo": "marcelo vieira da silva junior",
    "fernandinho": "fernando luiz rosa",
    "heung-min son": "son heung-min",
    "bryan ruiz": "bryan jafet ruiz gonzalez",
    "diego godin": "diego roberto godin leal",
    "marco urena": "marco danilo urena porras",
    "felipe baloy": "felipe abdiel baloy ramirez",
    "gylfi sigurdsson": "gylfi þor sigurðsson",
    "kendall waston": "kendall jamaal waston manley",
    "casemiro": "carlos henrique casimiro",
    "eric maxim choupo moting": "jean-eric maxim choupo-moting",
    "gue-sung cho": "cho gue-sung",
    "yeltsin tejeda": "yeltsin ignacio tejeda valverde",
    "giorgian de arrascaeta": "giorgian daniel de arrascaeta benedetti",
    "seung-ho paik": "paik seung-ho",
    "oghenekaro etebo": "etebo peter oghenekaro",
    "sergei ignashevich": "sergei nikolayevich ignashevich",
    "thiago cionek": "thiago rangel cionek",
    "denis cheryshev": "denis dmitriyevich cheryshev",
    "enzo fernandez": "enzo jeremias fernandez",
    # Alias adicionales conocidos
    "neymar": "neymar da silva santos junior",
    "neymar jr": "neymar da silva santos junior",
    "neymar jr.": "neymar da silva santos junior",
    "cristiano ronaldo": "cristiano ronaldo dos santos aveiro",
    "lionel messi": "lionel andres messi",
    "diego maradona": "diego armando maradona",
    "thierry henry": "thierry daniel henry",
    "paolo maldini": "paolo cesare maldini",
    "roberto carlos": "roberto carlos da silva rocha",
    "andres iniesta": "andres iniesta lujan",
    "sergio ramos": "sergio ramos garcia",
    "angel di maria": "angel fabian di maria hernandez",
    "manuel neuer": "manuel peter neuer",
    "mats hummels": "mats julian hummels",
    "thiago silva": "thiago emiliano da silva",
    "eden hazard": "eden michael hazard",
    "harry kane": "harry edward kane",
    "kylian mbappe": "kylian mbappe lottin",
    "philippe coutinho": "philippe coutinho correia",
    "raphael varane": "raphael xavier varane",
    "thibaut courtois": "thibaut nicolas marc courtois",
    "michel platini": "michel francois platini",
    "johan cruyff": "hendrik johannes cruijff",
    "johan cruijff": "hendrik johannes cruijff",
    "eric maxim choupo-moting": "jean-eric maxim choupo-moting",
}

# =====================================================
# Configuración
# =====================================================
HTML_BASE = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "..", "..", "..",  # sube a BASES_DE_DATOS_2_PROYECTO_GRUPO19
    "Fase1", "data", "202300512", "01-html"
)
HTML_BASE = os.path.normpath(HTML_BASE)

JUGADORES_SQL = os.path.join(
    os.path.dirname(__file__),
    "..", "..", "Nivel1", "03-jugador", "3jugador.sql"
)
JUGADORES_SQL = os.path.normpath(JUGADORES_SQL)

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "16evento_gol.sql")

# Regex para extraer minuto del alt del img de gol
GOL_ALT_RE = re.compile(r"Gol min (\d+(?:\+\d+)?)")

# Regex para extraer minuto del texto visible (ej: "23'" o "90'+2'")
GOL_MIN_TEXT_RE = re.compile(r"(\d+)'(?:\+(\d+)')?")


def normalize_name(name):
    """Normaliza un nombre para comparación: quita acentos, lowercase, espacios extra."""
    name = unicodedata.normalize("NFD", name)
    name = "".join(c for c in name if unicodedata.category(c) != "Mn")
    name = name.lower().strip()
    name = re.sub(r"\s+", " ", name)
    # Quitar apóstrofes escapados de SQL
    name = name.replace("''", "'")
    return name


def load_jugadores():
    """Carga el mapeo nombre -> id_ju desde 3jugador.sql."""
    jugadores = {}  # normalized_name -> id_ju
    jugadores_original = {}  # normalized_name -> nombre original

    if not os.path.exists(JUGADORES_SQL):
        print(f"[ERROR] No se encontró archivo de jugadores: {JUGADORES_SQL}")
        return jugadores, jugadores_original

    # Regex para extraer id y nombre del INSERT
    insert_re = re.compile(
        r"INSERT INTO Jugador\s*\([^)]+\)\s*VALUES\s*\(\s*(\d+)\s*,\s*'([^']*(?:''[^']*)*)'",
        re.IGNORECASE
    )

    with open(JUGADORES_SQL, "r", encoding="utf-8") as f:
        for line in f:
            match = insert_re.search(line)
            if match:
                id_ju = int(match.group(1))
                nombre = match.group(2).replace("''", "'")
                norm = normalize_name(nombre)
                jugadores[norm] = id_ju
                jugadores_original[norm] = nombre

    print(f"Jugadores cargados: {len(jugadores)}")
    return jugadores, jugadores_original


def limpiar_nombre_html(nombre_html):
    """Limpia sufijos como '(en contra)' del nombre del HTML."""
    nombre = re.sub(r"\s*\(en contra\)\s*", "", nombre_html, flags=re.IGNORECASE).strip()
    return nombre


def find_jugador_id(nombre_html, jugadores_dict):
    """Busca el id del jugador en el diccionario.
    1) Limpia '(en contra)' del nombre
    2) Busca en ALIAS_JUGADORES
    3) Coincidencia exacta normalizada
    4) Coincidencia parcial
    5) Coincidencia por apellido
    """
    nombre_limpio = limpiar_nombre_html(nombre_html)
    norm = normalize_name(nombre_limpio)

    # 1) Buscar en alias map
    if norm in ALIAS_JUGADORES:
        alias_norm = normalize_name(ALIAS_JUGADORES[norm])
        if alias_norm in jugadores_dict:
            return jugadores_dict[alias_norm]

    # 2) Coincidencia exacta
    if norm in jugadores_dict:
        return jugadores_dict[norm]

    # 3) Buscar por coincidencia parcial (el nombre del HTML puede ser abreviado)
    for db_name, db_id in jugadores_dict.items():
        if norm in db_name or db_name in norm:
            return db_id

    # 4) Buscar por apellido (último token)
    html_parts = norm.split()
    if html_parts:
        apellido = html_parts[-1]
        matches = [(k, v) for k, v in jugadores_dict.items() if k.split()[-1] == apellido]
        if len(matches) == 1:
            return matches[0][1]

        if len(html_parts) >= 2:
            nombre_first = html_parts[0]
            matches2 = [(k, v) for k, v in matches if nombre_first in k]
            if len(matches2) == 1:
                return matches2[0][1]

    return None


def parse_goles(filepath):
    """Extrae los goles de un archivo HTML de partido.

    Retorna lista de dicts: {jugador_nombre, tiempo_gol, entre_tiempo, penal}
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    soup = BeautifulSoup(content, "html.parser")

    # Buscar sección de GOLES: el div que contiene los goles está después
    # del comentario <!-- GOLES --> pero usamos el header "Goles:" como guía
    goles_header = soup.find("strong", string=re.compile(r"Goles:", re.IGNORECASE))
    if not goles_header:
        return []

    # El div principal de goles es el siguiente sibling del div que contiene "Goles:"
    goles_container = goles_header.find_parent("div")
    if goles_container:
        goles_container = goles_container.find_next_sibling("div")
    if not goles_container:
        return []

    results = []

    # Buscar todas las imgs con alt="Gol min X"
    gol_imgs = goles_container.find_all("img", alt=GOL_ALT_RE)

    for img in gol_imgs:
        alt = img.get("alt", "")
        alt_match = GOL_ALT_RE.search(alt)
        if not alt_match:
            continue

        tiempo_raw = alt_match.group(1)
        # Formatear: "90+2" está bien, "23" también
        tiempo_gol = tiempo_raw

        # Determinar si es penal y nombre del jugador
        # El jugador está en un div cercano al img
        parent_div = img.find_parent("div", class_=re.compile(r"w-50|left"))

        # Buscar en el ancestro que contiene el nombre
        # Subimos hasta el div con w-50
        w50_parent = img
        for _ in range(10):
            w50_parent = w50_parent.parent
            if w50_parent is None:
                break
            classes = w50_parent.get("class", [])
            if isinstance(classes, list):
                class_str = " ".join(classes)
            else:
                class_str = classes
            if "w-50" in class_str:
                break

        if w50_parent is None:
            continue

        # Extraer nombre del jugador y si es penal
        full_text = w50_parent.get_text(strip=True)

        # El texto tiene formato como: "23'Lionel Messi (de penal)" o "48'Saleh Al-Shehri"
        # Quitar el minuto del inicio
        nombre_text = re.sub(r"^\d+'(?:\+\d+')?", "", full_text).strip()

        es_penal = 0
        if "(de penal)" in nombre_text.lower() or "(de penal)" in full_text.lower():
            es_penal = 1
            nombre_text = re.sub(r"\s*\(de penal\)\s*", "", nombre_text, flags=re.IGNORECASE).strip()

        # Limpiar nombre: quitar cualquier residuo
        nombre_text = nombre_text.strip()
        if not nombre_text:
            continue

        # Determinar entre_tiempo
        min_base = int(re.match(r"(\d+)", tiempo_gol).group(1))
        entre_tiempo = "1" if min_base > 45 else "0"

        results.append({
            "jugador_nombre": nombre_text,
            "tiempo_gol": tiempo_gol,
            "entre_tiempo": entre_tiempo,
            "penal": es_penal,
        })

    return results


def main():
    print(f"Directorio HTML base: {HTML_BASE}")
    print(f"Archivo jugadores: {JUGADORES_SQL}")

    if not os.path.isdir(HTML_BASE):
        print(f"[ERROR] No existe el directorio: {HTML_BASE}")
        return

    # Cargar jugadores
    jugadores_dict, jugadores_original = load_jugadores()
    if not jugadores_dict:
        print("[ERROR] No se pudieron cargar los jugadores")
        return

    year_dirs = sorted([
        d for d in os.listdir(HTML_BASE)
        if os.path.isdir(os.path.join(HTML_BASE, d)) and d.isdigit()
    ])

    print(f"Mundiales encontrados: {len(year_dirs)}")

    inserts = []
    inconsistencias = []
    ev_pa_counter = 0
    id_ev_go = 1
    total_goles = 0
    partidos_sin_goles = 0
    jugadores_no_encontrados = 0

    for year_str in year_dirs:
        year_path = os.path.join(HTML_BASE, year_str)
        html_files = sorted(glob.glob(os.path.join(year_path, "*.html")))

        print(f"\n--- Mundial {year_str}: {len(html_files)} partidos ---")

        for html_file in html_files:
            ev_pa_counter += 1
            filename = os.path.basename(html_file)

            goles = parse_goles(html_file)

            if not goles:
                partidos_sin_goles += 1
                continue

            for g in goles:
                nombre_limpio = limpiar_nombre_html(g["jugador_nombre"])
                jugador_id = find_jugador_id(g["jugador_nombre"], jugadores_dict)

                if jugador_id is None:
                    jugadores_no_encontrados += 1
                    inconsistencias.append(
                        f"JUGADOR NO ENCONTRADO en {filename} (ev_pa={ev_pa_counter}): "
                        f"'{g['jugador_nombre']}' (limpio: '{nombre_limpio}') - gol al minuto {g['tiempo_gol']}"
                    )
                    continue

                entre_tiempo_val = f"'{g['entre_tiempo']}'" if g["entre_tiempo"] else "NULL"
                penal_val = g["penal"]

                insert = (
                    f"INSERT INTO Evento_Gol (id_ev_go, Evento_Partido_id_ev_pa, "
                    f"Jugador_id_ju, tiempo_gol, entre_tiempo_ev_go, penal) VALUES "
                    f"({id_ev_go}, {ev_pa_counter}, {jugador_id}, "
                    f"'{g['tiempo_gol']}', {entre_tiempo_val}, {penal_val});"
                )
                inserts.append((int(year_str), filename, insert))
                id_ev_go += 1
                total_goles += 1

    # Escribir archivo SQL
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("-- =====================================================\n")
        f.write("-- Evento_Gol: Goles de todos los mundiales\n")
        f.write("-- Generado automáticamente por scraper_evento_gol.py\n")
        f.write("-- =====================================================\n")
        f.write("-- Columnas:\n")
        f.write("--   id_ev_go                : ID autoincremental del gol\n")
        f.write("--   Evento_Partido_id_ev_pa : FK a Evento_Partido\n")
        f.write("--   Jugador_id_ju           : FK a Jugador\n")
        f.write("--   tiempo_gol              : Minuto del gol (ej: '23', '90+2')\n")
        f.write("--   entre_tiempo_ev_go      : '1' si segundo tiempo, '0' si primero\n")
        f.write("--   penal                   : 1 si fue de penal, 0 si no\n")
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
    print(f"Total goles procesados: {total_goles}")
    print(f"Partidos sin goles: {partidos_sin_goles}")
    print(f"Jugadores no encontrados: {jugadores_no_encontrados}")
    print(f"Inconsistencias: {len(inconsistencias)}")
    if inconsistencias:
        print("\nDetalle de inconsistencias:")
        for inc in inconsistencias:
            print(f"  - {inc.encode('ascii', 'replace').decode('ascii')}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
