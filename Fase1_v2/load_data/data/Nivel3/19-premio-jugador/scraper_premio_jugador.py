import os
import re
import unicodedata
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime
from collections import defaultdict
import difflib  # stdlib para fuzzy matching

BASE_HTML = Path(r"C:\Users\matth\OneDrive\Escritorio\datos\html")
RUTA_PROYECTO = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1")

RUTA_MUNDIAL_SQL = RUTA_PROYECTO / "04-mundial/4mundial.sql"
RUTA_JUGADOR_SQL = RUTA_PROYECTO / "03-jugador/3jugador.sql"
RUTA_pais_pre_SQL = RUTA_PROYECTO / "05-pais_pre/5pais_pre.sql"
RUTA_TIPO_PREMIO_SQL = RUTA_PROYECTO / "06-tipo-premio/6tipo_premio.sql"

OUT_PREMIO = Path("./8premios.sql")
OUT_PREMIOS_JUGADOR = Path("./20premios_jugador.sql")

# 🔧 FUZZY & ALIAS CONFIGURATION - MAP COMPLETO DE JUGADORES PROBLEMÁTICOS
# Reemplaza la sección ALIAS_JUGADORES (líneas 22-65) con esto:

ALIAS_JUGADORES = {
    # Alias existentes
    "pele": 6050,
    "pelé": 6050,
    
    # 🔥 NUEVOS: Map completo de jugadores que fallan → nombre EXACTO en 3jugador.sql
    "michele andreolo": "miguel andreolo frodella",  # id=429 ✓
    "miguel andreolo": "miguel andreolo frodella",   # id=429 ✓
    
    "garrincha": "manuel francisco dos santos",
    
    "bobby charlton": "sir robert charlton",
    
    "johan cruijff": "hendrik johannes cruijff",
    "johan cruyff": "hendrik johannes cruijff",
    
    "michel platini": "michel françois platini",
    
    "diego maradona": "diego armando maradona",
    
    "emilio butragueno": "emilio butragueño santos",  # sin ñ ni ú
    "emilio butragueño": "emilio butragueño santos",  # con ñ y ú
    "emilio butragueño": "emilio butragueño santos",  # doble seguridad
    
    "paolo maldini": "paolo cesare maldini",
    
    "roberto carlos": "roberto carlos da silva rocha",
    
    "ronaldinho": "ronaldo de assis moreira",
    "ronaldinho gaúcho": "ronaldo de assis moreira",
    "ronaldinho gaucho": "ronaldo de assis moreira",
    
    "thierry henry": "thierry daniel henry",
    
    "andres iniesta": "andrés iniesta luján",
    
    "maicon": "maicon douglas sisenando",
    
    "sergio ramos": "sergio ramos garcía",
    
    "xavi": "xavi simons",
    
    "angel di maria": "ángel fabián di maría hernández",
    "ángel di maría": "ángel fabián di maría hernández",
    
    "david luiz": "david luiz moreira marinho3",
    
    "lionel messi": "lionel andrés messi",
    
    "manuel neuer": "manuel peter neuer",
    
    "marcelo": "marcelo vieira da silva júnior",
    
    "mats hummels": "mats julian hummels",
    
    "neymar jr.": "neymar da silva santos júnior",
    "neymar jr": "neymar da silva santos júnior",
    "neymar": "neymar da silva santos júnior",
    
    "thiago silva": "thiago emiliano da silva",
    
    "cristiano ronaldo": "cristiano ronaldo dos santos aveiro",
    
    "diego godin": "diego roberto godín leal",
    
    "eden hazard": "eden michael hazard",
    
    "harry kane": "harry edward kane",
    
    "kylian mbappe": "kylian mbappé lottin",
    "kylian mbappé": "kylian mbappé lottin",
    
    "philippe coutinho": "philippe coutinho correia",
    
    "raphael varane": "raphaël xavier varane",
    "raphael xavier varane": "raphaël xavier varane",
    
    "romelu lukaku": "romelu menama lukaku bolingoli",
    
    "thibaut courtois": "thibaut nicolas marc courtois",
}

STOPWORDS_NO_JUGADORES = {
    "balon", "botin", "oro", "plata", "bronce", "goleador", "mejor", "guante"
}

def normalizar(texto: str) -> str:
    texto = texto.strip()
    texto = ''.join(
        c for c in unicodedata.normalize('NFD', texto)
        if unicodedata.category(c) != 'Mn'
    )
    return re.sub(r'\s+', ' ', texto).lower()

def log(msg: str):
    print(msg)

def buscar_jugador_fuzzy(nombre_norm, jugadores, umbral=0.85):
    """Busca jugador con fuzzy matching usando difflib (stdlib)"""
    nombres_norm = list(jugadores.keys())
    candidatos = difflib.get_close_matches(nombre_norm, nombres_norm, n=3, cutoff=umbral)
    if candidatos:
        mejor_key = candidatos[0]
        jug_data = jugadores[mejor_key]
        log(f"[FUZZY✓] '{nombre_norm}' → '{jug_data['nombre']}' (id={jug_data['id']}, score≈{umbral*100:.0f}%)")
        return jug_data
    return None

def cargar_mundiales():
    mundiales = {}
    patron = re.compile(r"VALUES\s*\((\d+),\s*(\d+),")
    with open(RUTA_MUNDIAL_SQL, encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                id_mu = int(m.group(1))
                anio = int(m.group(2))
                mundiales[anio] = id_mu
    log(f"[DEBUG] Mundiales cargados: {mundiales}")
    return mundiales

def cargar_jugadores():
    """Ahora retorna dict con nombre_original e id"""
    jugadores = {}
    patron = re.compile(r"VALUES\s*\((\d+),\s*'([^']*)'")
    with open(RUTA_JUGADOR_SQL, encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                id_ju = int(m.group(1))
                nombre = m.group(2)
                key = normalizar(nombre)
                jugadores[key] = {
                    "id": id_ju,
                    "nombre": nombre,
                }
    log(f"[DEBUG] Total jugadores cargados: {len(jugadores)}")
    for i, (k, v) in enumerate(list(jugadores.items())[:10]):
        log(f"[DEBUG] Jugador ejemplo {i+1}: '{k}' -> '{v['nombre']}' (id={v['id']})")
    return jugadores

def cargar_pais_prees():
    pais_prees = {}
    patron = re.compile(r"VALUES\s*\((\d+),\s*'([^']*)'")
    with open(RUTA_pais_pre_SQL, encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                id_pa = int(m.group(1))
                nombre = m.group(2)
                pais_prees[normalizar(nombre)] = id_pa
    log(f"[DEBUG] Total países cargados: {len(pais_pre_prees)}")
    for i, (k, v) in enumerate(list(pais_prees.items())[:10]):
        log(f"[DEBUG] País ejemplo {i+1}: '{k}' -> {v}")
    return pais_prees

def cargar_tipo_premio():
    por_nombre_exact = {}
    por_nombre_norm = {}
    patron = re.compile(r"VALUES\s*\((\d+),\s*'([^']*)'")
    with open(RUTA_TIPO_PREMIO_SQL, encoding="utf-8") as f:
        for linea in f:
            m = patron.search(linea)
            if m:
                id_ti = int(m.group(1))
                nombre = m.group(2).strip()
                por_nombre_exact[nombre] = id_ti
                por_nombre_norm[normalizar(nombre)] = id_ti
    log(f"[DEBUG] Tipo_Premio exact: {por_nombre_exact}")
    log(f"[DEBUG] Tipo_Premio norm: {por_nombre_norm}")
    return por_nombre_exact, por_nombre_norm

def parsear_html_premios(path_html: Path):
    with open(path_html, encoding="utf-8") as f:
        soup = BeautifulSoup(f.read(), "html.parser")

    log(f"[DEBUG] --- Analizando HTML: {path_html.name} ---")

    bloques = soup.find_all('div', style=re.compile(r'BEA388'))
    if not bloques:
        bloques = soup.find_all('div', style=re.compile(r'border:\s*1px\s*solid'))
    log(f"[DEBUG] Bloques de premios encontrados: {len(bloques)}")

    premios = []

    for idx, bloque in enumerate(bloques, start=1):
        titulo = bloque.find('p', class_='negri')
        if not titulo:
            log(f"[DEBUG] Bloque {idx}: sin <p class='negri'>, se omite.")
            continue

        nombre_premio_html = titulo.get_text(strip=True)
        nombre_norm = normalizar(nombre_premio_html)
        log(f"[DEBUG] Bloque {idx}: título='{nombre_premio_html}' (norm='{nombre_norm}')")

        # CASO ESPECIAL 1: FIFA Fair Play
        if "fair play" in nombre_norm:
            img_bandera = bloque.find('img', src=re.compile(r'banderas/'))
            if img_bandera and img_bandera.get('alt'):
                pais_pre_html = img_bandera['alt'].strip()
                log(f"[DEBUG]  -> Fair Play, país='{pais_pre_html}'")
                premios.append({
                    'nombre_premio_html': nombre_premio_html,
                    'jugadores': [],
                    'pais_pre': pais_pre_html
                })
            else:
                log(f"[DEBUG]  -> Fair Play SIN país (no se añade)")
            continue

        # CASO ESPECIAL 2: EQUIPO IDEAL - DIVIDIR EN 4 PREMIOS
        if "equipo ideal" in nombre_norm:
            log(f"[DEBUG]  -> CASO ESPECIAL: Equipo Ideal, dividiendo por posiciones...")
            
            posiciones = {
                'arquero': 'Equipo Ideal (Arquero)',
                'defensores': 'Equipo Ideal (Defensores)',
                'mediocampistas': 'Equipo Ideal (Mediocampistas)',
                'delanteros': 'Equipo Ideal (Delanteros)'
            }
            
            secciones = {pos: [] for pos in posiciones}
            seccion_actual = None

            for elemento in bloque.find_all(text=True):
                texto_norm = normalizar(elemento)
                if any(pos in texto_norm for pos in posiciones):
                    for pos_key, pos_nombre in posiciones.items():
                        if pos_key in texto_norm:
                            seccion_actual = pos_key
                            log(f"[DEBUG]     -> Sección detectada: '{pos_key}'")
                            break
                elif seccion_actual and elemento.parent.name == 'a' and 'jugadores/' in elemento.parent.get('href', ''):
                    nombre_jug = elemento.parent.get_text(strip=True)
                    secciones[seccion_actual].append(nombre_jug)
                    log(f"[DEBUG]     -> Jugador en {seccion_actual}: '{nombre_jug}'")

            for pos, nombre_premio in posiciones.items():
                if secciones[pos]:
                    log(f"[DEBUG]     -> Creando '{nombre_premio}' con {len(secciones[pos])} jugadores")
                    premios.append({
                        'nombre_premio_html': nombre_premio,
                        'jugadores': secciones[pos],
                        'pais_pre': None
                    })

            continue

        # CASOS NORMALES
        subbloques = bloque.find_all('div', class_=re.compile(r'rd-100-30'))
        if subbloques:
            log(f"[DEBUG]  -> Bloque {idx} tiene {len(subbloques)} sub-bloques rd-100-30")
            for sidx, sub in enumerate(subbloques, start=1):
                titulo_sub = sub.find('p', class_='negri')
                if not titulo_sub:
                    log(f"[DEBUG]   Subbloque {sidx}: sin <p class='negri'>, se omite.")
                    continue
                nombre_sub = titulo_sub.get_text(strip=True)
                nombre_sub_norm = normalizar(nombre_sub)

                p_detalle = sub.find('p', class_=re.compile(r'margen-b0'))
                links = []
                if p_detalle:
                    links = p_detalle.find_all('a', href=re.compile(r'jugadores/'))

                if not links:
                    texto = sub.get_text(" ", strip=True)
                    candidatos = re.findall(r'[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+)*', texto)
                    log(f"[DEBUG]   Subbloque {sidx} '{nombre_sub}': sin links; candidatos por regex={candidatos}")
                    if candidatos:
                        candidato_norm = normalizar(candidatos[0])
                        if candidato_norm in STOPWORDS_NO_JUGADORES:
                            log(f"[DEBUG]   ❌ Candidato '{candidatos[0]}' descartado (stopword, premio vacío)")
                            continue
                        premios.append({
                            'nombre_premio_html': nombre_sub,
                            'jugadores': [candidatos[0]],
                            'pais_pre': None
                        })
                    continue

                nombres_jug = [a.get_text(strip=True) for a in links if a.get_text(strip=True)]
                log(f"[DEBUG]   Subbloque {sidx} '{nombre_sub}': jugadores={nombres_jug}")
                if nombres_jug:
                    premios.append({
                        'nombre_premio_html': nombre_sub,
                        'jugadores': nombres_jug,
                        'pais_pre': None
                    })
            continue

        # 🔥 NUEVO: BLOQUE SIN SUBBLOQUES = premio único (Guante / Mejor Joven)
        # Aquí 'bloque' ya es el contenedor con border (w-90-sm)
        p_detalle = bloque.find('p', class_=re.compile(r'margen-b0'))
        links = []
        if p_detalle:
            links = p_detalle.find_all('a', href=re.compile(r'jugadores/'))

        nombres_jug = [a.get_text(strip=True) for a in links if a.get_text(strip=True)]
        log(f"[DEBUG]  -> Bloque {idx} SIN subbloques, premio simple '{nombre_premio_html}': jugadores={nombres_jug}")

        if nombres_jug:
            premios.append({
                'nombre_premio_html': nombre_premio_html,
                'jugadores': nombres_jug,
                'pais_pre': None
            })

        continue


    log(f"[DEBUG] Premios parseados en {path_html.name}:")
    for p in premios:
        log(f"   [DEBUG] Premio: '{p['nombre_premio_html']}', pais_pre={p['pais_pre']}, jugadores={len(p['jugadores'])} jugadores")
    return premios

def main():
    log("📥 Cargando mappings desde SQL...")
    mundiales = cargar_mundiales()
    jugadores = cargar_jugadores()
    pais_prees = cargar_pais_prees()
    tipo_pre_exact, tipo_pre_norm = cargar_tipo_premio()

    log(f"[DEBUG] Mundiales totales: {len(mundiales)}")
    log(f"[DEBUG] Jugadores totales: {len(jugadores)}")
    log(f"[DEBUG] Países totales:    {len(pais_prees)}")
    log(f"[DEBUG] TiposPremio totales: {len(tipo_pre_exact)}")

    inserts_premio = []
    inserts_pre_ju = []
    next_id_pre = 1
    premio_existente = {}
    warnings = []

    for path_html in sorted(BASE_HTML.glob("*_premios*.html")):
        m = re.search(r'(\d{4})', path_html.name)
        if not m:
            log(f"[DEBUG] Archivo {path_html.name} no tiene año en el nombre, se omite.")
            continue
        anio = int(m.group(1))
        id_mundial = mundiales.get(anio)
        if not id_mundial:
            w = f"-- ADVERTENCIA: Mundial {anio} no está en 4mundial.sql"
            log(f"[WARN] {w}")
            warnings.append(w)
            continue

        log(f"\n🏆 Procesando {path_html.name} (Mundial {anio}, id={id_mundial})")

        premios_html = parsear_html_premios(path_html)
        log(f"[DEBUG] Total premios detectados en HTML {anio}: {len(premios_html)}")

        for premio in premios_html:
            nombre_html = premio['nombre_premio_html']
            nombre_norm = normalizar(nombre_html)
            log(f"[DEBUG]  Manejo de premio '{nombre_html}' (norm='{nombre_norm}')")

            id_tipo_premio = tipo_pre_exact.get(nombre_html)
            if not id_tipo_premio:
                id_tipo_premio = tipo_pre_norm.get(nombre_norm)
            log(f"[DEBUG]   -> id_tipo_premio resuelto={id_tipo_premio}")

            if not id_tipo_premio:
                w = f"-- ADVERTENCIA [{anio}]: Tipo_Premio no encontrado para '{nombre_html}'"
                log(f"[WARN] {w}")
                warnings.append(w)
                continue

            # FAIR PLAY
            if "fair play" in nombre_norm and premio['pais_pre']:
                pais_pre_norm = normalizar(premio['pais_pre'])
                id_pais_pre = pais_prees.get(pais_pre_norm)
                log(f"[DEBUG]   -> Fair Play país='{premio['pais_pre']}' norm='{pais_pre_norm}' id_pais_pre={id_pais_pre}")
                if not id_pais_pre:
                    w = f"-- ADVERTENCIA [{anio}] Fair Play: país no encontrado '{premio['pais_pre']}'"
                    log(f"[WARN] {w}")
                    warnings.append(w)
                    continue

                clave = (id_mundial, id_tipo_premio, id_pais_pre)
                if clave not in premio_existente:
                    id_pre = next_id_pre
                    next_id_pre += 1
                    premio_existente[clave] = id_pre

                    log(f"[DEBUG]   -> CREANDO Premio Fair Play id_pre={id_pre}")
                    inserts_premio.append(
                        f"-- {nombre_html}: {premio['pais_pre']} (Mundial {anio})\n"
                        f"INSERT INTO Premio (id_pre, Mundial_id_mu, pais_pre, Tipo_Premio_id_ti_pre) "
                        f"VALUES ({id_pre}, {id_mundial}, '{premio['pais_pre']}', {id_tipo_premio});"
                    )
                else:
                    log(f"[DEBUG]   -> Premio Fair Play ya existía, id_pre={premio_existente[clave]}")
                continue

            # Resto: premios con jugadores
            if not premio['jugadores']:
                log(f"[DEBUG]   -> Premio SIN jugadores, se omite.")
                continue

            clave = (id_mundial, id_tipo_premio, None)
            if clave not in premio_existente:
                id_pre = next_id_pre
                next_id_pre += 1
                premio_existente[clave] = id_pre

                log(f"[DEBUG]   -> CREANDO Premio normal id_pre={id_pre}")
                inserts_premio.append(
                    f"-- {nombre_html} (Mundial {anio})\n"
                    f"INSERT INTO Premio (id_pre, Mundial_id_mu, pais_pre_pre, Tipo_Premio_id_ti_pre) "
                    f"VALUES ({id_pre}, {id_mundial}, NULL, {id_tipo_premio});"
                )
            else:
                id_pre = premio_existente[clave]
                log(f"[DEBUG]   -> Premio ya existente id_pre={id_pre}")

            # 🔥 VINCULAR JUGADORES CON ALIAS MAP + FUZZY (NUEVA LÓGICA)
            for nombre_jug_html in premio['jugadores']:
                key = normalizar(nombre_jug_html)
                
                # Filtrar Balón/Botín
                if key in STOPWORDS_NO_JUGADORES:
                    log(f"[DEBUG]    ❌ Omitiendo '{nombre_jug_html}' (es '{key}', premio vacío)")
                    continue

                id_jug = None
                
                # 1️⃣ ALIAS MANUAL COMPLETO (nuevo map)
                if key in ALIAS_JUGADORES:
                    alias_val = ALIAS_JUGADORES[key]
                    
                    # Si es ID directo (int)
                    if isinstance(alias_val, int):
                        id_jug = alias_val
                        log(f"[ALIAS-ID✓] '{nombre_jug_html}' → id={id_jug} (alias directo)")
                    else:
                        # Si es nombre completo → buscar en jugadores
                        alias_key = normalizar(alias_val)
                        if alias_key in jugadores:
                            jug_data = jugadores[alias_key]
                            id_jug = jug_data["id"]
                            log(f"[ALIAS✓] '{nombre_jug_html}' → '{jug_data['nombre']}' (id={id_jug}) (via map)")
                        else:
                            log(f"[ALIAS✗] '{nombre_jug_html}' → '{alias_val}' no encontrado en jugadores")
                
                # 2️⃣ BÚSQUEDA EXACTA
                elif key in jugadores:
                    jug_data = jugadores[key]
                    id_jug = jug_data["id"]
                    log(f"[EXACT✓] '{nombre_jug_html}' → '{jug_data['nombre']}' (id={id_jug})")
                
                # 3️⃣ FUZZY MATCHING
                elif (jug_data := buscar_jugador_fuzzy(key, jugadores, umbral=0.85)):
                    id_jug = jug_data["id"]
                
                # 4️⃣ FALLA → WARNING
                if not id_jug:
                    w = f"-- ADVERTENCIA [{anio}] [{nombre_html}]: Jugador no encontrado '{nombre_jug_html}'"
                    log(f"[❌] [{anio}] {nombre_html}: '{nombre_jug_html}' (norm='{key}')")
                    warnings.append(w)
                    continue

                inserts_pre_ju.append(
                    f"INSERT INTO Premios_Jugador (Premio_id_pre, Jugador_id_ju) "
                    f"VALUES ({id_pre}, {id_jug});"
                )

    # ── REPORTE FINAL ────────────────────────────────
    log("\n" + "="*80)
    log("📊 REPORTE FINAL: JUGADORES NO ENCONTRADOS")
    log("="*80)

    no_encontrados_por_nombre = defaultdict(list)
    no_encontrados_por_mundial = defaultdict(list)

    for w in warnings:
        if "Jugador no encontrado" in w:
            match = re.search(r'\[(\d+)\]\s*\[([^\]]+)\]:\s*Jugador no encontrado\s*\'([^\']+)\'', w)
            if match:
                mundial, premio, nombre_html = match.groups()
                nombre_norm = normalizar(nombre_html)
                
                # Filtrar Balón/Botín del reporte final
                if nombre_norm in STOPWORDS_NO_JUGADORES:
                    log(f"[DEBUG] Reporte: omitiendo '{nombre_html}' (stopword)")
                    continue
                
                no_encontrados_por_nombre[nombre_html].append((mundial, premio))
                no_encontrados_por_mundial[mundial].append(nombre_html)
            else:
                log(f"[ERROR] Warning no parseada: {w}")

    log(f"\n🔍 TOTAL JUGADORES FALLIDOS: {len(no_encontrados_por_nombre)} únicos")
    if no_encontrados_por_mundial:
        log(f"📈 JUGADORES por MUNDIAL:")
        for mundial, lista in sorted(no_encontrados_por_mundial.items()):
            unicos = sorted(set(lista))
            log(f"  {mundial}: {len(unicos)} únicos → {unicos}")

    log(f"\n👥 RESUMEN por JUGADOR (con premios donde falló):")
    for nombre_html in sorted(no_encontrados_por_nombre.keys()):
        apariciones = no_encontrados_por_nombre[nombre_html]
        mundiales = set([m[0] for m in apariciones])
        premios = set([m[1] for m in apariciones])
        log(f"  '{nombre_html}' → {len(mundiales)} mundial(es), {len(premios)} premio(s)")
        for m, p in apariciones[:3]:
            log(f"    → {m} [{p}]")

    log("="*80 + "\n")

    # ── GENERAR ARCHIVOS SQL ────────────────────────────────────────────────────
    log("\n💾 Generando archivos SQL...")

    contenido_premio = [
        "-- 8premios.sql – generado automáticamente",
        f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "",
    ]
    if warnings:
        contenido_premio.extend(["-- Advertencias:", *warnings, ""])
    contenido_premio.extend(inserts_premio)
    OUT_PREMIO.write_text("\n".join(contenido_premio) + "\n", encoding="utf-8")

    contenido_pj = [
        "-- 20premios_jugador.sql – generado automáticamente",
        f"-- Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "-- Requiere que 8premios.sql se haya ejecutado antes",
        "",
    ]
    contenido_pj.extend(inserts_pre_ju)
    OUT_PREMIOS_JUGADOR.write_text("\n".join(contenido_pj) + "\n", encoding="utf-8")

    log(f"✅ Listo!")
    log(f"   Premios generados: {len(inserts_premio)}")
    log(f"   Premios_Jugador generados: {len(inserts_pre_ju)}")
    log(f"   → {OUT_PREMIO.absolute()}")
    log(f"   → {OUT_PREMIOS_JUGADOR.absolute()}")

if __name__ == "__main__":
    main()
