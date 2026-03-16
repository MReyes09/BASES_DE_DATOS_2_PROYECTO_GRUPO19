import os
import re
import unicodedata
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from datetime import datetime


# 📁 RUTAS ACTUALIZADAS
BASE_DIR = Path(r"C:\Users\matth\OneDrive\Escritorio\datos\html")
RUTA_MUNDIAL_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\4mundial.sql")
RUTA_JUGADOR_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\3jugador.sql")
RUTA_PAIS_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\5pais.sql")
RUTA_TIPO_PREMIO_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\6tipo_premio.sql")

OUT_PREMIO = Path("./8premios.sql")
OUT_PREMIOS_JUGADOR = Path("./20premios_jugador.sql")

# 🔒 LOCK para thread-safe writing
lock = threading.Lock()
resultados = {"premios": [], "premios_jugador": [], "next_id_pre": 1, "premio_existente": {}}

def log_status(mensaje):
    """Imprime con timestamp en vivo"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {mensaje}")

def normalizar_nombre(nombre):
    nombre = nombre.strip()
    nombre = ''.join(c for c in unicodedata.normalize('NFD', nombre)
                     if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', nombre).lower()

# ================================
# PRE-CARGAR MAPPINGS (SINGLE THREAD)
# ================================
def cargar_mappings():
    log_status("📥 Cargando mappings desde SQL...")
    
    # Mundial
    mundial_map = {}
    with open(RUTA_MUNDIAL_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*(\d+),", linea)
            if match:
                id_mu, anio = int(match.group(1)), int(match.group(2))
                mundial_map[anio] = id_mu
    
    # Jugador
    jugador_map = {}
    with open(RUTA_JUGADOR_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*'([^']*)'", linea)
            if match:
                id_ju = int(match.group(1))
                nombre_raw = match.group(2)
                nombre_norm = normalizar_nombre(nombre_raw)
                jugador_map[nombre_norm] = id_ju
    
    # País
    pais_map = {}
    with open(RUTA_PAIS_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*'([^']*)'", linea)
            if match:
                id_pa = int(match.group(1))
                nombre_raw = match.group(2)
                nombre_norm = normalizar_nombre(nombre_raw)
                pais_map[nombre_norm] = id_pa
    
    # Tipo Premio
    tipo_premio_map = {}
    with open(RUTA_TIPO_PREMIO_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*'([^']*)'", linea)
            if match:
                id_ti_pre = int(match.group(1))
                nombre = match.group(2).strip()
                tipo_premio_map[nombre] = id_ti_pre
    
    log_status(f"✅ Mappings: {len(mundial_map)} Mundiales, {len(jugador_map)} Jugadores, {len(pais_map)} Países, {len(tipo_premio_map)} Premios")
    return mundial_map, jugador_map, pais_map, tipo_premio_map

# ================================
# 🎯 PROCESAR HTML CORREGIDO (SOLO Fair Play → país)
# ================================
# ← REEMPLAZA la función procesar_html COMPLETA

def procesar_html(archivo_html, mappings):
    mundial_map, jugador_map, pais_map, tipo_premio_map = mappings
    
    try:
        anio_match = re.search(r'(\d{4})_premios', archivo_html.name)
        if not anio_match:
            return []
        
        anio = int(anio_match.group(1))
        log_status(f"  🔄 Procesando {archivo_html.name} ({anio})")
        
        id_mundial = mundial_map.get(anio)
        if not id_mundial:
            log_status(f"    ❌ Mundial {anio} no encontrado")
            return []
        
        with open(archivo_html, 'r', encoding='utf-8') as f:
            html = f.read()
        
        soup = BeautifulSoup(html, 'html.parser')
        bloques_premios = soup.find_all('div', style=re.compile(r'BEA388'))
        premios_extraidos = []
        
        for bloque in bloques_premios:
            titulo_premio = bloque.find('p', class_='negri')
            if not titulo_premio:
                continue
                
            nombre_premio = titulo_premio.get_text(strip=True)
            pais_nombre_norm = None
            
            # 🎯 DETECTAR TODOS los Fair Play (múltiples formatos)
            if any(frase in nombre_premio for frase in ['Fair Play', 'fair play', 'FAIR PLAY']):
                # Buscar bandera (Fair Play = país)
                img = bloque.find('img', src=re.compile(r'banderas/'))
                if img and img.get('alt'):
                    pais_nombre_norm = normalizar_nombre(img.get('alt'))
                    log_status(f"    🏆 FAIR PLAY '{img.get('alt')}' → {pais_nombre_norm}")
                    premios_extraidos.append((nombre_premio, None, pais_nombre_norm))
                else:
                    log_status(f"    ⚠️  Fair Play '{nombre_premio}' SIN bandera")
            
            # Resto de premios = jugadores
            else:
                links_jugadores = bloque.find_all('a', href=re.compile(r'jugadores/'))
                if links_jugadores:
                    for link in links_jugadores:
                        nombre_jugador = link.get_text(strip=True)
                        premios_extraidos.append((nombre_premio, nombre_jugador, None))
                else:
                    log_status(f"    ❓ Premio '{nombre_premio}' sin jugadores")
        
        log_status(f"    ✅ {len(premios_extraidos)} premios encontrados")
        return (anio, id_mundial, premios_extraidos)
        
    except Exception as e:
        log_status(f"    ❌ Error en {archivo_html.name}: {e}")
        return []

# ================================
# MAIN CON HILOS
# ================================
def generar_inserts_sql():
    log_status("🚀 INICIANDO SCRAPER PREMIOS FIFA (MULTI-HILO)")
    log_status("=" * 60)
    
    # 1. Cargar mappings
    mappings = cargar_mappings()
    
    # 2. Encontrar archivos HTML
    archivos_html = list(BASE_DIR.glob("*_premios*"))
    log_status(f"📂 Encontrados {len(archivos_html)} archivos HTML")
    
    if not archivos_html:
        log_status("❌ No se encontraron archivos *_premios*.html")
        return
    
    # 3. PROCESAR EN PARALELO (8 hilos máx)
    log_status("⚡ Procesando en paralelo...")
    with ThreadPoolExecutor(max_workers=8) as executor:
        resultados_html = list(executor.map(
            lambda archivo: procesar_html(archivo, mappings), 
            archivos_html
        ))
    
    mundial_map, jugador_map, pais_map, tipo_premio_map = mappings
    
    # 4. GENERAR INSERTS (single thread para evitar race conditions)
    log_status("✍️  Generando INSERTs SQL...")
    
    with lock:
        for resultado in resultados_html:
            if not resultado:
                continue
                
            anio, id_mundial, premios_extraidos = resultado
            
            for nombre_premio, nombre_jugador, pais_nombre_norm in premios_extraidos:
                id_tipo_premio = tipo_premio_map.get(nombre_premio)
                if not id_tipo_premio:
                    continue
                
                clave_premio = (id_mundial, id_tipo_premio)
                if clave_premio not in resultados["premio_existente"]:
                    id_pre = resultados["next_id_pre"]
                    resultados["next_id_pre"] += 1
                    resultados["premio_existente"][clave_premio] = id_pre
                    
                    # ✅ FIX f-string + SOLO Fair Play tiene país
                    pais_insert = "NULL"
                    if pais_nombre_norm:
                        pais_insert = "'{}'".format(pais_nombre_norm.replace("'", "''"))
                    
                    resultados["premios"].append(
                        "INSERT INTO Premio (id_pre, Mundial_id_mu, pais_pre, Tipo_Premio_id_ti_pre) "
                        "VALUES ({}, {}, {}, {});".format(
                            id_pre, id_mundial, pais_insert, id_tipo_premio
                        )
                    )
                
                id_pre = resultados["premio_existente"][clave_premio]
                
                if nombre_jugador:
                    nombre_norm = normalizar_nombre(nombre_jugador)
                    id_jugador = jugador_map.get(nombre_norm)
                    if id_jugador:
                        resultados["premios_jugador"].append(
                            "INSERT INTO Premios_Jugador (Premio_id_pre, Jugador_id_ju) "
                            "VALUES ({}, {});".format(id_pre, id_jugador)
                        )
    
    # 5. GUARDAR ARCHIVOS (FIX f-string)
    log_status("💾 Guardando archivos SQL...")
    
    contenido_premio = (
        "-- 🏆 PREMIOS FIFA - Generados automáticamente (SOLO Fair Play tiene pais_pre)\n"
        "-- id_pre inicia en 1, finaliza en " + str(resultados['next_id_pre']-1) + "\n"
        "-- Ejecutado: " + datetime.now().strftime('%Y-%m-%d %H:%M:%S') + "\n\n"
        + "\n".join(resultados["premios"]) + "\n"
    )
    OUT_PREMIO.write_text(contenido_premio, encoding='utf-8')
    
    contenido_jugador = (
        "-- 🏆 PREMIOS FIFA - Jugadores ganadores\n"
        "-- Requiere que se hayan insertado Premios primero\n\n"
        + "\n".join(resultados["premios_jugador"]) + "\n"
    )
    OUT_PREMIOS_JUGADOR.write_text(contenido_jugador, encoding='utf-8')
    
    log_status("✅ ¡SCRAPER COMPLETADO!")
    log_status(f"📊 {len(resultados['premios'])} INSERTs Premio")
    log_status(f"📊 {len(resultados['premios_jugador'])} INSERTs Premios_Jugador")
    log_status(f"💾 {OUT_PREMIO}")
    log_status(f"💾 {OUT_PREMIOS_JUGADOR}")
    log_status("⚡ Tiempo: MULTI-HILO (8 workers)")

if __name__ == "__main__":
    generar_inserts_sql()
