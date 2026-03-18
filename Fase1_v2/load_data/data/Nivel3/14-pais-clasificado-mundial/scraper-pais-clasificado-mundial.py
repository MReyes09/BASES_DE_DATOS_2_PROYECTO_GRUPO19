import re
import unicodedata
import difflib
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime


# ─────────────────────────────────────────────
#  RUTAS
# ─────────────────────────────────────────────
BASE_HTML        = Path(r"C:\Users\DILAN\Documents\USAC\Bases2\Archivos\html_grupos\html")
RUTA_SQL         = Path(r"C:\Users\DILAN\Documents\USAC\Bases2\Proyecto\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1")

RUTA_MUNDIAL_SQL = RUTA_SQL / "04-mundial/4mundial.sql"
RUTA_PAIS_SQL    = RUTA_SQL / "05-pais/5pais.sql"
RUTA_GRUPO_SQL   = RUTA_SQL / "02-grupo/2grupo.sql"

OUT_SQL = Path("./pais_clasificado_mundial.sql")


# ─────────────────────────────────────────────
#  ALIAS DE PAISES (nombre en HTML -> nombre exacto en 5pais.sql)
# ─────────────────────────────────────────────
ALIAS_PAISES = {
    "checoslovaquia"                  : "Checoslovaquia",
    "paises bajos"                    : "Países Bajos",
    "holanda"                         : "Países Bajos",
    "estados unidos"                  : "Estados Unidos",
    "corea del sur"                   : "Corea del Sur",
    "corea del norte"                 : "Corea del Norte",
    "arabia saudita"                  : "Arabia Saudita",
    "costa de marfil"                 : "Costa de Marfil",
    "republica checa"                 : "República Checa",
    "alemania occidental"             : "Alemania Occidental",
    "alemania oriental"               : "Alemania Oriental",
    "republica democratica del congo" : "República Democrática del Congo",
    "trinidad y tobago"               : "Trinidad y Tobago",
    "emiratos arabes unidos"          : "Emiratos Árabes Unidos",
    "irlanda del norte"               : "Irlanda del Norte",
    "bosnia-herzegovina"              : "Bosnia-Herzegovina",
    "union sovietica"                 : "URSS",
    "urss"                            : "URSS",
    "yugoslavia"                      : "Yugoslavia",
    "zaire"                           : "Zaire",
    "iran"                            : "Irán",
    "tunez"                           : "Túnez",
    "belgica"                         : "Bélgica",
    "japon"                           : "Japón",
    # ── FIXES de advertencias reportadas ──────
    "iraq"                            : "Irak",                   # [1986] HTML='Iraq'            -> id=51
    "emiratos arabes"                 : "Emiratos Árabes Unidos", # [1990] HTML='Emiratos Arabes'  -> id=41
    "serbia y montenegro"             : "Serbia",                 # [2006] HTML='Serbia y Montenegro' -> id=85
}

# Grupos especiales que NO son fases clasificatorias (ronda final 1950, etc.)
GRUPOS_IGNORAR = {"f", "final", "semifinal", "3er", "3ro"}


# ─────────────────────────────────────────────
#  UTILIDADES
# ─────────────────────────────────────────────
def normalizar(texto):
    texto = texto.strip()
    texto = "".join(
        c for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )
    return re.sub(r"\s+", " ", texto).lower()


def log(msg):
    print(msg)


# ─────────────────────────────────────────────
#  CARGA DE MAPPINGS DESDE SQL
# ─────────────────────────────────────────────
def cargar_mundiales():
    """Retorna {anio: id_mundial}"""
    mundiales = {}
    patron = re.compile(r"VALUES\s*\((\d+),\s*(\d+),")
    with open(RUTA_MUNDIAL_SQL, encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                mundiales[int(m.group(2))] = int(m.group(1))
    log(f"[DEBUG] Mundiales cargados: {mundiales}")
    return mundiales


def cargar_paises():
    """Retorna {nombre_norm: id_pais}"""
    paises = {}
    patron = re.compile(r"VALUES\s*\((\d+),\s*'([^']*)'")
    with open(RUTA_PAIS_SQL, encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                id_pa  = int(m.group(1))
                nombre = m.group(2)
                key    = normalizar(nombre)
                if key not in paises:   # evitar duplicados, queda el primer id
                    paises[key] = id_pa
    log(f"[DEBUG] Paises cargados: {len(paises)}")
    return paises


def cargar_grupos():
    """
    Retorna {nombre_grupo_norm: id_gr}
    Ejemplos: 'a'->1, 'b'->2, ..., 'h'->8, '1'->9, '2'->10, '3'->11, '4'->12
    """
    grupos = {}
    patron = re.compile(r"VALUES\s*\((\d+),\s*'([^']*)'")
    with open(RUTA_GRUPO_SQL, encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                id_gr  = int(m.group(1))
                nombre = m.group(2).strip()
                grupos[normalizar(nombre)] = id_gr
    log(f"[DEBUG] Grupos cargados: {grupos}")
    return grupos


# ─────────────────────────────────────────────
#  RESOLUCION DE PAIS  (exact -> alias -> fuzzy)
# ─────────────────────────────────────────────
def resolver_pais(nombre_html, paises, umbral=0.82):
    norm = normalizar(nombre_html)

    # 1. Exacto
    if norm in paises:
        log(f"[EXACT] '{nombre_html}' -> id={paises[norm]}")
        return paises[norm]

    # 2. Alias manual
    alias_nombre = ALIAS_PAISES.get(norm)
    if alias_nombre:
        norm2 = normalizar(alias_nombre)
        if norm2 in paises:
            log(f"[ALIAS] '{nombre_html}' -> '{alias_nombre}' -> id={paises[norm2]}")
            return paises[norm2]

    # 3. Fuzzy matching
    candidatos = difflib.get_close_matches(norm, list(paises.keys()), n=3, cutoff=umbral)
    if candidatos:
        mejor = candidatos[0]
        log(f"[FUZZY] '{nombre_html}' -> '{mejor}' -> id={paises[mejor]}")
        return paises[mejor]

    log(f"[ERROR] Pais no encontrado: '{nombre_html}'")
    return None


def resolver_grupo(num_grupo_raw, grupos):
    """
    Recibe el texto del HTML ('1','A','B'...) y devuelve id_gr
    desde el dict cargado de 2grupo.sql.
    """
    key   = normalizar(str(num_grupo_raw))
    id_gr = grupos.get(key)
    if id_gr:
        log(f"[GRUPO] '{num_grupo_raw}' -> id_gr={id_gr}")
    else:
        log(f"[ERROR] Grupo no encontrado: '{num_grupo_raw}'")
    return id_gr


# ─────────────────────────────────────────────
#  PARSEO DEL HTML - EXTRAE GRUPOS Y PAISES
# ─────────────────────────────────────────────
def parsear_grupos(path_html):
    """
    Extrae lista de (texto_grupo, nombre_pais) desde la tabla de grupos.
    Estructura HTML:
      <tr class="a-top">
        <td class="w-1-12 negri pad-t2">1</td>   <- numero/letra de grupo
        <td ...>link resultados</td>
        <td class="d-flex flex-wrap">
          <div ...>
            <a href="../planteles/...">
              <img alt="NombrePais"><br> NombrePais
            </a>
          </div>
        </td>
      </tr>
    """
    with open(path_html, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    resultados = []

    for tr in soup.find_all("tr", class_="a-top"):
        tds = tr.find_all("td", recursive=False)
        if len(tds) < 3:
            continue

        # 1er TD = numero/letra de grupo
        num_grupo_raw = tds[0].get_text(strip=True)
        if not num_grupo_raw:
            continue

        # Ignorar rondas especiales (Grupo F = ronda final 1950, etc.)
        if normalizar(num_grupo_raw) in GRUPOS_IGNORAR:
            log(f"[SKIP] Grupo '{num_grupo_raw}' ignorado (ronda especial)")
            continue

        # 3er TD = contenedor de paises
        td_paises = tds[2]

        for div in td_paises.find_all("div"):
            nombre_pais = None

            # Preferir el alt del img (más limpio)
            img = div.find("img")
            if img and img.get("alt"):
                nombre_pais = img["alt"].strip()

            # Fallback: último texto del link <a>
            if not nombre_pais:
                a = div.find("a")
                if a:
                    textos = [t.strip() for t in a.stripped_strings]
                    if textos:
                        nombre_pais = textos[-1]

            if nombre_pais and normalizar(nombre_pais):
                resultados.append((num_grupo_raw, nombre_pais))
                log(f"[DEBUG]   Grupo '{num_grupo_raw}' -> '{nombre_pais}'")

    return resultados


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
def main():
    log("Cargando mappings SQL...")
    mundiales = cargar_mundiales()
    paises    = cargar_paises()
    grupos    = cargar_grupos()

    inserts  = []
    warnings = []

    archivos = sorted(set(
        list(BASE_HTML.glob("*_mundial*.HTML")) +
        list(BASE_HTML.glob("*_mundial*.html"))
    ))

    if not archivos:
        log("[WARN] No se encontraron archivos HTML.")

    for path_html in archivos:
        m = re.search(r"(\d{4})", path_html.name)
        if not m:
            log(f"[WARN] Sin anio en: {path_html.name}")
            continue

        anio       = int(m.group(1))
        id_mundial = mundiales.get(anio)

        if not id_mundial:
            w = f"-- ADVERTENCIA: Mundial {anio} no encontrado en 4mundial.sql"
            log(f"[WARN] {w}")
            warnings.append(w)
            continue

        log(f"\nProcesando: {path_html.name}  (Mundial {anio}, id_mu={id_mundial})")

        grupos_paises = parsear_grupos(path_html)
        log(f"[DEBUG] Registros encontrados: {len(grupos_paises)}")

        vistos = set()

        for num_grupo_raw, nombre_html in grupos_paises:

            # Resolver id_gr desde 2grupo.sql
            id_gr = resolver_grupo(num_grupo_raw, grupos)
            if not id_gr:
                w = f"-- ADVERTENCIA [{anio}]: Grupo no resuelto '{num_grupo_raw}'"
                log(f"[WARN] {w}")
                warnings.append(w)
                continue

            # Resolver id_pa desde 5pais.sql
            id_pais = resolver_pais(nombre_html, paises)
            if not id_pais:
                w = f"-- ADVERTENCIA [{anio}] Grupo '{num_grupo_raw}': Pais no resuelto '{nombre_html}'"
                log(f"[WARN] {w}")
                warnings.append(w)
                continue

            # Evitar duplicados
            clave = (id_mundial, id_pais, id_gr)
            if clave in vistos:
                log(f"[SKIP] Duplicado: Mundial={anio}, Pais='{nombre_html}', Grupo='{num_grupo_raw}'")
                continue
            vistos.add(clave)

            inserts.append(
                f"-- {nombre_html} | Grupo {num_grupo_raw} | Mundial {anio}\n"
                f"INSERT INTO Pais_Clasificado_Mundial (Mundial_id_mu, Pais_id_pa, Grupo_id_gr) "
                f"VALUES ({id_mundial}, {id_pais}, {id_gr});"
            )

    # ── Generar archivo SQL ──
    contenido = [
        "-- pais_clasificado_mundial.sql  -  generado automaticamente",
        f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"-- Total inserts: {len(inserts)}",
        "",
    ]
    if warnings:
        contenido += ["-- ── ADVERTENCIAS ──", *warnings, ""]

    contenido += inserts

    OUT_SQL.write_text("\n".join(contenido) + "\n", encoding="utf-8")

    log("\n" + "=" * 70)
    log(f"Inserts generados  : {len(inserts)}")
    log(f"Advertencias       : {len(warnings)}")
    log(f"Archivo generado   : {OUT_SQL.absolute()}")
    log("=" * 70)


if __name__ == "__main__":
    main()
