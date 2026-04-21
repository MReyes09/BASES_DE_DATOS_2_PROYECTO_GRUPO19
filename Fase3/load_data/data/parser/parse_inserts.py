# parse_inserts.py
import re, json
from datetime import datetime
from pathlib import Path

OUTPUT = Path("json_output")
OUTPUT.mkdir(exist_ok=True)

def parse_sql_file(filepath):
    """Lee un .sql de inserts y retorna lista de dicts"""
    text = Path(filepath).read_text(encoding="utf-8", errors="ignore")
    # Extrae VALUES de cada INSERT
    pattern = re.compile(
        r"INSERT\s+INTO\s+\w+\s*(?:\([^)]+\))?\s*VALUES\s*\((.+?)\)\s*;",
        re.IGNORECASE | re.DOTALL
    )
    rows = []
    for match in pattern.finditer(text):
        raw = match.group(1)
        # Parsea los valores respetando strings con comas adentro
        values = parse_values(raw)
        rows.append(values)
    return rows

def parse_values(raw):
    """Parsea una fila de VALUES respetando strings entre comillas simples"""
    values = []
    current = ""
    in_string = False
    i = 0
    while i < len(raw):
        c = raw[i]
        if c == "'" and not in_string:
            in_string = True
            current += c
        elif c == "'" and in_string:
            # Maneja '' (escape de comilla en Oracle)
            if i + 1 < len(raw) and raw[i+1] == "'":
                current += "'"
                i += 2
                continue
            in_string = False
            current += c
        elif c == "," and not in_string:
            values.append(clean_value(current.strip()))
            current = ""
        else:
            current += c
        i += 1
    values.append(clean_value(current.strip()))
    return values

def clean_value(v):
    """Convierte string SQL a valor Python"""
    if v.upper() == "NULL":
        return None
    if v.startswith("'") and v.endswith("'"):
        return v[1:-1].replace("''", "'")
    # TO_DATE
    m = re.match(r"TO_DATE\('(.+?)',\s*'(.+?)'\)", v, re.IGNORECASE)
    if m:
        try:
            return datetime.strptime(m.group(1), m.group(2).replace("DD","d").replace("MM","m").replace("YYYY","Y")).strftime("%Y-%m-%d")
        except:
            return m.group(1)
    try:
        return int(v)
    except ValueError:
        try:
            return float(v)
        except ValueError:
            return v

# Mapeo: nombre_archivo -> columnas en orden
TABLES = {
    "1fase":          ["id_fa", "nombre_fa"],
    "2grupo":         ["id_gr", "nombre_gr"],
    "3jugador":       ["id_ju", "nombre_ju", "fecha_nacimiento_ju", "lugar_nacimiento_ju", "altura_ju", "apodo_ju", "pagina_web_ju"],
    "4mundial":       ["id_mu", "anio_mu", "organizador_mu"],
    "5pais":          ["id_pa", "name_pa"],
    "6tipo_premio":   ["id_ti_pre", "nombre_ti_pre"],
    "7tipo_tarjeta":  ["id_ti_ta", "color_tarjeta"],
    "8premios":        ["id_pre", "Mundial_id_mu", "pais_pre", "Tipo_Premio_id_ti_pre", "entrenador_pre"],
    "9red_social":    ["id_red_so", "nombre_red_so", "tipo_red_sp", "Jugador_id_ju"],
    "10plantilla":     ["id_pla", "Pais_id_pa", "director_tecnico_pla"],
    "11llave_mundial": ["Mundial_id_mu", "Fase_id_fa"],
    "12evento_partido":["id_ev_pa", "fecha_ev_pa", "Llave_Mundial_id_mu", "Llave_Mundial_id_fa"],
    "13evento_cambio_jugador": ["id_ev_ca_ju", "Evento_Partido_id_ev_pa"],
    "14pais_clasificado_mundial": ["Mundial_id_mu", "Pais_id_pa", "Grupo_id_gr"],
    "15evento_falta":  ["id_ev_fa", "Evento_Partido_id_ev_pa", "Tipo_Tarjeta_id_ti_ta", "minuto_falta", "entre_tiempo"],
    "16evento_gol":    ["id_ev_go", "Evento_Partido_id_ev_pa", "Jugador_id_ju", "tiempo_gol", "entre_tiempo_ev_go", "penal"],
    "17partido_plantilla": ["Plantilla_id_pla", "Evento_Partido_id_ev_pa"],
    "18posicionjugador": ["Plantilla_id_pla", "Jugador_id_ju", "nombre_po_ju", "capitan", "no_camiseta", "titular"],
    "19premios_jugador": ["Premio_id_pre", "Jugador_id_ju"],
    "20cambio_jugador":  ["id_ca_ju", "Evento_Cambio_Jugador_id_ev_ca_ju", "Jugador_id_ju", "tiempo_ca_ju"],
}

for filename, columns in TABLES.items():
    path = Path(f"{filename}.sql")
    if not path.exists():
        print(f"  [SKIP] {filename}.sql no encontrado")
        continue
    rows = parse_sql_file(path)
    docs = [dict(zip(columns, row)) for row in rows]
    out = OUTPUT / f"{filename}.json"
    with open(out, "w", encoding="utf-8") as f:
        json.dump(docs, f, ensure_ascii=False, indent=2)
    print(f"  [OK] {filename}.json — {len(docs)} documentos")

print("\nListo! Revisa la carpeta json_output/")