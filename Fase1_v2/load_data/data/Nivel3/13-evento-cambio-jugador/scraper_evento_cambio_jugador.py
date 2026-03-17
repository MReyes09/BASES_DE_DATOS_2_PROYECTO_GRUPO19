"""
Scraper para generar INSERTs de Evento_Cambio_Jugador y Cambio_Jugador.
Lee los HTMLs de partidos y extrae la sección "Cambios" de cada uno.

Tablas destino:
    Evento_Cambio_Jugador(id_ev_ca_ju, Evento_Partido_id_ev_pa)
    Cambio_Jugador(Evento_Cambio_Jugador_id_ev_ca_ju, Jugador_id_ju, tiempo_ca_ju)

Cada cambio genera:
    - 1 registro en Evento_Cambio_Jugador
    - 2 registros en Cambio_Jugador (jugador que ingresa + jugador que sale)

Uso:
    python scraper_evento_cambio_jugador.py
"""

import os
import re
import glob
import unicodedata
import difflib
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

JUGADOR_SQL = Path(
    r"c:\Users\danie.000\Documents\BD2\Projecto1\BASES_DE_DATOS_2_PROYECTO_GRUPO19"
    r"\Fase1_v2\load_data\data\Nivel1\03-jugador\3jugador.sql"
)

OUTPUT_EVENTO = BASE_DIR / "13evento_cambio_jugador.sql"
OUTPUT_CAMBIO = BASE_DIR.parent / "20-cambio-jugador" / "20cambio_jugador.sql"

# Mapeo de apodos/nombres cortos del HTML -> nombre completo en la BD
ALIAS_JUGADOR = {
    "Bobby Charlton": "Sir Robert Charlton",
    "Ronaldinho": "Ronaldo de Assis Moreira",
    "Kaká": "Ricardo Izecson dos Santos Leite",
    "Kaka": "Ricardo Izecson dos Santos Leite",
    "Hulk": "Givanildo Vieira de Souza",
    "Fernandinho": "Fernando Luiz Rosa",
    "Juanito": "Juan Gomez",
    "Tim Cahill": "Timothy Filiga Cahill",
    "Mark Bresciano": "Marco Bresciano",
    "Xabi Alonso": "Xabier Alonso Olano",
    "Johan Djourou": "Johan Danon Djourou-Gbadjere",
    "Mile Jedinak": "Michael John Jedinak",
    "Dani Alves": "Daniel Alves da Silva",
    "Eric Maxim Choupo Moting": "Jean-Eric Maxim Choupo-Moting",
    "Eric Maxim Choupo-Moting": "Jean-Eric Maxim Choupo-Moting",
    "El Arabi Soudani": "El Arbi Hillel Soudani",
    "Khamis Al Dossari": "Khamis Al-Owairan Al-Dossari",
    "Dani Shmulevich-Rom": "Daniel Shmulevich-Rom",
    "Goikoetxea": "Jon Andoni Goikoetxea Lasa",
    "Abdullah Zubromawi": "Abdullah Sulaiman Zubromawi",
    "Diego Maradona": "Diego Armando Maradona",
    "Faustino Asprilla": "Faustino Hernan Asprilla Hinestroza",
    "Marcelo Gallardo": "Marcelo Daniel Gallardo",
    "Gabriel Batistuta": "Gabriel Omar Batistuta",
    "David Beckham": "David Robert Joseph Beckham",
    "Thierry Henry": "Thierry Daniel Henry",
    "Michel Platini": "Michel Francois Platini",
    "Enzo Francescoli": "Enzo Francescoli Uriarte",
    "Neymar": "Neymar da Silva Santos Junior",
    "Neymar Jr.": "Neymar da Silva Santos Junior",
    "Coutinho": "Philippe Coutinho Correia",
    "Fred": "Frederico Chaves Guedes",
    "Oscar": "Oscar dos Santos Emboaba Junior",
    "Jo": "Joao Alves de Assis Silva",
    "Jô": "Joao Alves de Assis Silva",
    "Isco": "Francisco Roman Alarcon Suarez",
    "Nacho": "Jose Ignacio Fernandez Iglesias",
    "Pepe": "Kepler Laveran de Lima Ferreira",
    "Raphael Guerreiro": "Raphael Adelino Jose Guerreiro",
    "Adama Traoré": "Adama Traore",
    "Dani Olmo": "Daniel Olmo Carvajal",
    "Pedri": "Pedro Gonzalez Lopez",
    "Gavi": "Pablo Martin Paez Gavira",
    "Samuel Umtiti": "Samuel Yves Umtiti",
    "Alisson": "Alisson Ramses Becker",
    "Ederson": "Ederson Santana de Moraes",
    "Casemiro": "Carlos Henrique Venancio Casimiro",
    "Marquinhos": "Marcos Aoás Corrêa",
    "Willian": "Willian Borges da Silva",
    "Ramires": "Ramires Santos do Nascimento",
    "Dani Carvajal": "Daniel Carvajal Ramos",
    "Koke": "Jorge Resurreccion Merodio",
    "Saul": "Saul Niguez Esclapez",
    "Vitinha": "Vitor Machado Ferreira",
    "Bruno Fernandes": "Bruno Miguel Borges Fernandes",
    "Bernardo Silva": "Bernardo Mota Veiga de Carvalho e Silva",
    "Joao Felix": "Joao Felix Sequeira",
    "Diogo Jota": "Diogo Jose Teixeira da Silva",
    "Son Heung-min": "Son Heung-min",
    "Manuel Jimenez": "Manuel Jimenez",
    "Danny Welbeck": "Daniel Nii Tackie Mensah Welbeck",
    "Christian Stuani": "Cristhian Ricardo Stuani Curbelo",
    "Mahmoud Kahraba": "Mahmoud Abdel-Moneim",
    "Danny Rose": "Daniel Lee Rose",
    "Dele Alli": "Bamidele Jermaine Alli",
    "Casemiro": "Carlos Henrique Casimiro",
    "Alex Iwobi": "Alexander Chuka Iwobi",
    "Sam Morsy": "Samy Sayed Morsy",
    "Saeid Ezatolahi": "Saeed Ezatolahi Afagh",
    "Nordin Amrabat": "Noureddine Amrabat",
    "Tom Rogic": "Tomas Petar Rogic",
}


def cargar_jugadores():
    """Carga el mapeo nombre_jugador -> id_ju desde el SQL de jugadores."""
    mapa = {}
    pattern = re.compile(
        r"VALUES\s*\(\s*(\d+),\s*'([^']*(?:''[^']*)*)'",
        re.I
    )

    with open(JUGADOR_SQL, encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if "INSERT INTO Jugador" not in linea:
                continue
            m = pattern.search(linea)
            if m:
                id_ju = int(m.group(1))
                nombre = m.group(2).replace("''", "'")
                if nombre not in mapa:
                    mapa[nombre] = id_ju

    print(f"{len(mapa)} jugadores cargados desde SQL")
    return mapa


def normalizar_nombre(nombre):
    """Normaliza un nombre para comparación: quita acentos, minúsculas, espacios extra."""
    nombre = nombre.strip()
    # Reemplazar caracteres corruptos comunes (encoding issues)
    nombre = nombre.replace('\ufffd', '')
    # Decompose unicode and remove combining marks
    nfkd = unicodedata.normalize('NFKD', nombre)
    result = ''.join(c for c in nfkd if not unicodedata.combining(c))
    return re.sub(r'\s+', ' ', result).lower().strip()


def construir_indices_jugadores(jugadores):
    """
    Construye múltiples índices para buscar jugadores:
    1. Exacto: nombre_completo -> id
    2. Normalizado: nombre_normalizado -> id
    3. Por contención: para buscar "Thierry Henry" dentro de "Thierry Daniel Henry"
    """
    idx_exacto = dict(jugadores)  # ya es nombre -> id
    idx_norm = {}
    idx_lista = []  # lista de (nombre_norm, nombre_partes_norm, id_ju)

    for nombre_sql, id_ju in jugadores.items():
        norm = normalizar_nombre(nombre_sql)
        if norm not in idx_norm:
            idx_norm[norm] = id_ju
        partes = set(norm.split())
        idx_lista.append((norm, partes, id_ju, nombre_sql))

    return idx_exacto, idx_norm, idx_lista


def buscar_jugador_id(nombre_html, idx_exacto, idx_norm, idx_lista):
    """Busca el id del jugador usando múltiples estrategias."""
    nombre = nombre_html.strip()

    # 0. Verificar alias primero (soporta nombre string o ID directo)
    if nombre in ALIAS_JUGADOR:
        alias = ALIAS_JUGADOR[nombre]
        if isinstance(alias, int):
            return alias
        if alias in idx_exacto:
            return idx_exacto[alias]
        norm_alias = normalizar_nombre(alias)
        if norm_alias in idx_norm:
            return idx_norm[norm_alias]

    # 1. Coincidencia exacta
    if nombre in idx_exacto:
        return idx_exacto[nombre]

    # 2. Coincidencia normalizada exacta
    norm_html = normalizar_nombre(nombre)
    if norm_html in idx_norm:
        return idx_norm[norm_html]

    # 3. Contención: el nombre HTML está contenido en el nombre SQL completo
    #    Ej: "Thierry Henry" está en "Thierry Daniel Henry"
    partes_html = norm_html.split()
    candidatos = []
    for norm_sql, partes_sql, id_ju, nombre_sql in idx_lista:
        # Todas las partes del nombre HTML deben estar en el nombre SQL
        if all(p in partes_sql for p in partes_html):
            candidatos.append((len(partes_sql), id_ju, nombre_sql))

    if len(candidatos) == 1:
        return candidatos[0][1]

    # Si hay múltiples candidatos, preferir el que tiene menos partes extra
    if candidatos:
        candidatos.sort(key=lambda x: x[0])
        return candidatos[0][1]

    # 4. Contención parcial: el nombre HTML normalizado es substring del SQL
    candidatos2 = []
    for norm_sql, _, id_ju, nombre_sql in idx_lista:
        if norm_html in norm_sql:
            candidatos2.append((len(norm_sql), id_ju, nombre_sql))

    if len(candidatos2) == 1:
        return candidatos2[0][1]

    if candidatos2:
        candidatos2.sort(key=lambda x: x[0])
        return candidatos2[0][1]

    # 5. Fuzzy matching con difflib (mismo enfoque que scraper_premio.py)
    nombres_norm = list(idx_norm.keys())
    matches = difflib.get_close_matches(norm_html, nombres_norm, n=1, cutoff=0.85)
    if matches:
        return idx_norm[matches[0]]

    return None


def extraer_cambios_de_html(filepath):
    """
    Extrae los cambios de un HTML de partido.
    Retorna lista de dicts: {jugador_in, jugador_out, minuto}
    """
    cambios = []

    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')

    # Buscar la sección "Cambios"
    h3 = soup.find("h3", string=re.compile(r"Cambios", re.I))
    if not h3:
        return cambios

    # Verificar si hay "ninguno"
    container = h3.find_parent("div")
    if not container:
        return cambios

    text_after = container.get_text()
    if "ninguno" in text_after.lower() and container.find("table") is None:
        return cambios

    # Buscar la tabla de cambios
    table = container.find("table", class_="a-left")
    if not table:
        return cambios

    rows = table.find_all("tr")
    for row in rows:
        # Saltar headers de país (tr class="bt-2")
        if "bt-2" in row.get("class", []):
            continue

        tds = row.find_all("td")
        if len(tds) < 5:
            continue

        # Extraer minuto del primer td
        minuto_div = tds[0].find("div", class_="d-inline-block")
        if not minuto_div:
            continue

        minuto_text = minuto_div.get_text(strip=True)
        if not minuto_text:
            continue

        # Limpiar el minuto (quitar "(en el entretiempo)" si existe)
        minuto_clean = minuto_text.replace("(en el entretiempo)", "").strip()

        # Extraer jugador que ingresa (td index 2) y jugador que sale (td index 4)
        jugador_in = tds[2].get_text(strip=True)
        jugador_out = tds[4].get_text(strip=True)

        if jugador_in and jugador_out:
            cambios.append({
                'jugador_in': jugador_in,
                'jugador_out': jugador_out,
                'minuto': minuto_clean,
            })

    return cambios


def main():
    print("SCRAPER EVENTO_CAMBIO_JUGADOR + CAMBIO_JUGADOR")
    print("=" * 60)

    if not os.path.isdir(HTML_BASE):
        print(f"[ERROR] No existe el directorio: {HTML_BASE}")
        return

    jugadores = cargar_jugadores()
    idx_exacto, idx_norm, idx_lista = construir_indices_jugadores(jugadores)

    # Obtener directorios de años (mismo orden que scraper_evento_partido.py)
    year_dirs = sorted([
        d for d in os.listdir(HTML_BASE)
        if os.path.isdir(os.path.join(HTML_BASE, d)) and d.isdigit()
    ])

    print(f"Mundiales encontrados: {len(year_dirs)}")

    inserts_evento = []   # (year, insert_sql)
    inserts_cambio = []   # (year, insert_sql)
    id_ev_pa = 1          # Mismo contador que scraper_evento_partido.py
    id_ev_ca_ju = 1       # ID autoincremental para Evento_Cambio_Jugador
    id_ca_ju = 1          # ID autoincremental para Cambio_Jugador
    total_cambios = 0
    sin_match = 0
    errores_detalle = []
    jugadores_no_encontrados = {}  # nombre -> set de archivos donde aparece

    for year_str in year_dirs:
        year = int(year_str)
        year_path = os.path.join(HTML_BASE, year_str)
        html_files = sorted(glob.glob(os.path.join(year_path, "*.html")))

        year_cambios = 0

        for html_file in html_files:
            cambios = extraer_cambios_de_html(html_file)
            filename = os.path.basename(html_file)

            for cambio in cambios:
                jugador_in_id = buscar_jugador_id(
                    cambio['jugador_in'], idx_exacto, idx_norm, idx_lista
                )
                jugador_out_id = buscar_jugador_id(
                    cambio['jugador_out'], idx_exacto, idx_norm, idx_lista
                )

                if jugador_in_id is None:
                    nombre_in = cambio['jugador_in']
                    errores_detalle.append(
                        f"  [WARN] Jugador IN no encontrado: '{nombre_in}' "
                        f"en {filename}"
                    )
                    jugadores_no_encontrados.setdefault(nombre_in, set()).add(filename)
                    sin_match += 1
                    continue

                if jugador_out_id is None:
                    nombre_out = cambio['jugador_out']
                    errores_detalle.append(
                        f"  [WARN] Jugador OUT no encontrado: '{nombre_out}' "
                        f"en {filename}"
                    )
                    jugadores_no_encontrados.setdefault(nombre_out, set()).add(filename)
                    sin_match += 1
                    continue

                # Truncar minuto a 8 caracteres (VARCHAR2(8))
                minuto = cambio['minuto'][:8]

                # INSERT Evento_Cambio_Jugador
                inserts_evento.append((year, (
                    f"INSERT INTO Evento_Cambio_Jugador (id_ev_ca_ju, "
                    f"Evento_Partido_id_ev_pa) VALUES "
                    f"({id_ev_ca_ju}, {id_ev_pa});"
                )))

                # INSERT Cambio_Jugador - jugador que ingresa
                inserts_cambio.append((year, (
                    f"INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, "
                    f"Jugador_id_ju, tiempo_ca_ju) VALUES "
                    f"({id_ca_ju}, {id_ev_ca_ju}, {jugador_in_id}, '{minuto}');"
                )))
                id_ca_ju += 1

                # INSERT Cambio_Jugador - jugador que sale
                inserts_cambio.append((year, (
                    f"INSERT INTO Cambio_Jugador (id_ca_ju, Evento_Cambio_Jugador_id_ev_ca_ju, "
                    f"Jugador_id_ju, tiempo_ca_ju) VALUES "
                    f"({id_ca_ju}, {id_ev_ca_ju}, {jugador_out_id}, '{minuto}');"
                )))
                id_ca_ju += 1

                id_ev_ca_ju += 1
                year_cambios += 1
                total_cambios += 1

            id_ev_pa += 1

        print(f"  Mundial {year_str}: {year_cambios} cambios")

    # Escribir archivo SQL de Evento_Cambio_Jugador
    os.makedirs(OUTPUT_EVENTO.parent, exist_ok=True)
    with open(OUTPUT_EVENTO, "w", encoding="utf-8") as f:
        f.write("-- =====================================================\n")
        f.write("-- Evento_Cambio_Jugador: Eventos de cambio por partido\n")
        f.write("-- Generado automáticamente por scraper_evento_cambio_jugador.py\n")
        f.write("-- =====================================================\n")
        f.write("-- Columnas:\n")
        f.write("--   id_ev_ca_ju             : ID autoincremental del evento de cambio\n")
        f.write("--   Evento_Partido_id_ev_pa : FK a Evento_Partido (id_ev_pa)\n")
        f.write(f"-- Total: {total_cambios} registros\n")
        f.write("-- =====================================================\n\n")

        current_year = None
        for year, insert in inserts_evento:
            if year != current_year:
                if current_year is not None:
                    f.write("\n")
                f.write(f"-- Mundial {year}\n")
                current_year = year
            f.write(f"{insert}\n")

    # Escribir archivo SQL de Cambio_Jugador
    os.makedirs(OUTPUT_CAMBIO.parent, exist_ok=True)
    with open(OUTPUT_CAMBIO, "w", encoding="utf-8") as f:
        f.write("-- =====================================================\n")
        f.write("-- Cambio_Jugador: Jugadores involucrados en cambios\n")
        f.write("-- Generado automáticamente por scraper_evento_cambio_jugador.py\n")
        f.write("-- =====================================================\n")
        f.write("-- Columnas:\n")
        f.write("--   Evento_Cambio_Jugador_id_ev_ca_ju : FK a Evento_Cambio_Jugador\n")
        f.write("--   Jugador_id_ju                     : FK a Jugador (id_ju)\n")
        f.write("--   tiempo_ca_ju                      : Minuto del cambio\n")
        f.write(f"-- Total: {total_cambios * 2} registros (2 por cada cambio)\n")
        f.write("-- =====================================================\n\n")

        current_year = None
        for year, insert in inserts_cambio:
            if year != current_year:
                if current_year is not None:
                    f.write("\n")
                f.write(f"-- Mundial {year}\n")
                current_year = year
            f.write(f"{insert}\n")

    print(f"\n{'=' * 60}")
    print(f"Total cambios procesados: {total_cambios}")
    print(f"Jugadores sin match: {sin_match}")
    print(f"Archivo generado: {OUTPUT_EVENTO}")
    print(f"Archivo generado: {OUTPUT_CAMBIO}")

    if errores_detalle:
        print(f"\nDetalle de jugadores no encontrados ({len(errores_detalle)}):")
        for err in errores_detalle[:50]:
            try:
                print(err)
            except UnicodeEncodeError:
                print(err.encode('ascii', 'replace').decode('ascii'))
        if len(errores_detalle) > 50:
            print(f"  ... y {len(errores_detalle) - 50} más")


if __name__ == "__main__":
    main()
