import os
import re
import unicodedata
from pathlib import Path
from bs4 import BeautifulSoup

# 📁 RUTAS ACTUALIZADAS
BASE_DIR = Path(r"C:\Users\matth\OneDrive\Escritorio\datos\html")  # ← CAMBIADO
RUTA_MUNDIAL_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\4mundial.sql")
RUTA_JUGADOR_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\3jugador.sql")
RUTA_PAIS_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\5pais.sql")  # ← NUEVO
RUTA_TIPO_PREMIO_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\6tipo_premio.sql")

OUT_PREMIO = Path(r"C:\Users\matth\Desktop\premios_auto.sql")
OUT_PREMIOS_JUGADOR = Path(r"C:\Users\matth\Desktop\premios_jugador_auto.sql")

def normalizar_nombre(nombre):
    nombre = nombre.strip()
    nombre = ''.join(c for c in unicodedata.normalize('NFD', nombre)
                     if unicodedata.category(c) != 'Mn')
    return re.sub(r'\s+', ' ', nombre).lower()

def parse_mundial_sql():
    mapping = {}
    with open(RUTA_MUNDIAL_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*(\d+),", linea)
            if match:
                id_mu, anio = int(match.group(1)), int(match.group(2))
                mapping[anio] = id_mu
    return mapping

def parse_jugador_sql():
    mapping = {}
    with open(RUTA_JUGADOR_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*'([^']*)'", linea)
            if match:
                id_ju = int(match.group(1))
                nombre_raw = match.group(2)
                nombre_norm = normalizar_nombre(nombre_raw)
                mapping[nombre_norm] = id_ju
    print(f"✅ Cargados {len(mapping)} jugadores")
    return mapping

def parse_pais_sql():
    """NUEVO: Mapea nombre_pais → id_pa"""
    mapping = {}
    with open(RUTA_PAIS_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*'([^']*)'", linea)
            if match:
                id_pa = int(match.group(1))
                nombre_raw = match.group(2)
                nombre_norm = normalizar_nombre(nombre_raw)
                mapping[nombre_norm] = id_pa
    print(f"✅ Cargados {len(mapping)} países")
    return mapping

def parse_tipo_premio_sql():
    mapping = {}
    with open(RUTA_TIPO_PREMIO_SQL, 'r', encoding='utf-8') as f:
        for linea in f:
            match = re.search(r"VALUES\s*\((\d+),\s*'([^']*)'", linea)
            if match:
                id_ti_pre = int(match.group(1))
                nombre = match.group(2).strip()
                mapping[nombre] = id_ti_pre
    print(f"✅ Cargados {len(mapping)} tipos de premio")
    return mapping

def extraer_pais_bandera(bloque):
    """Extrae nombre del país del atributo alt de la bandera"""
    img = bloque.find('img', src=re.compile(r'banderas/'))
    if img and img.get('alt'):
        pais_nombre = img.get('alt').strip()
        return normalizar_nombre(pais_nombre)
    return None

def extraer_premios_html(html_content, anio):
    soup = BeautifulSoup(html_content, 'html.parser')
    premios = []
    
    # Buscar TODOS los bloques de premios
    bloques_premios = soup.find_all('div', style=re.compile(r'BEA388'))
    
    for bloque in bloques_premios:
        titulo_premio = bloque.find('p', class_='negri')
        if not titulo_premio:
            continue
            
        nombre_premio = titulo_premio.get_text(strip=True)
        pais_nombre_norm = extraer_pais_bandera(bloque)
        
        # CASO ESPECIAL: FIFA Fair Play (solo país)
        if 'FIFA Fair Play' in nombre_premio and pais_nombre_norm:
            premios.append((nombre_premio, None, pais_nombre_norm))  # sin jugador
            continue
        
        # Buscar links de jugadores
        links_jugadores = bloque.find_all('a', href=re.compile(r'jugadores/'))
        for link in links_jugadores:
            nombre_jugador = link.get_text(strip=True)
            premios.append((nombre_premio, nombre_jugador, pais_nombre_norm))
    
    return premios

def generar_inserts_sql():
    # Cargar todos los mappings
    mundial_map = parse_mundial_sql()
    jugador_map = parse_jugador_sql()
    pais_map = parse_pais_sql()  # ← NUEVO
    tipo_premio_map = parse_tipo_premio_sql()
    
    inserts_premio = []
    inserts_premios_jugador = []
    
    next_id_pre = 1  # Ajusta según tu seq_premio_id_pre
    premio_existente = {}  # (id_mu, id_tipo) → id_pre
    
    print("\n🔍 Procesando HTMLs...")
    
    for archivo_html in sorted(BASE_DIR.glob("*_premios*")):
        anio_match = re.search(r'(\d{4})_premios', archivo_html.name)
        if not anio_match:
            continue
            
        anio = int(anio_match.group(1))
        print(f"  📄 {archivo_html.name} ({anio})")
        
        id_mundial = mundial_map.get(anio)
        if not id_mundial:
            print(f"    ❌ No encontrado Mundial {anio}")
            continue
            
        with open(archivo_html, 'r', encoding='utf-8') as f:
            html = f.read()
            
        premios_extraidos = extraer_premios_html(html, anio)
        
        for nombre_premio, nombre_jugador, pais_nombre_norm in premios_extraidos:
            id_tipo_premio = tipo_premio_map.get(nombre_premio)
            if not id_tipo_premio:
                print(f"    ⚠️  Tipo premio no encontrado: '{nombre_premio}'")
                continue
            
            # Crear Premio (siempre, incluso sin jugador para Fair Play)
            clave_premio = (id_mundial, id_tipo_premio)
            if clave_premio not in premio_existente:
                id_pre = next_id_pre
                next_id_pre += 1
                premio_existente[clave_premio] = id_pre
                
                # 👉 AGREGAR pais_pre (NULL si no hay)
                pais_insert = f"'{pais_nombre_norm.replace(''", "''")}'" if pais_nombre_norm else 'NULL'
                
                inserts_premio.append(
                    f"INSERT INTO Premio (id_pre, Mundial_id_mu, pais_pre, Tipo_Premio_id_ti_pre) "
                    f"VALUES ({id_pre}, {id_mundial}, {pais_insert}, {id_tipo_premio});"
                )
            
            id_pre = premio_existente[clave_premio]
            
            # Si HAY jugador, crear relación
            if nombre_jugador:
                nombre_norm = normalizar_nombre(nombre_jugador)
                id_jugador = jugador_map.get(nombre_norm)
                if id_jugador:
                    inserts_premios_jugador.append(
                        f"INSERT INTO Premios_Jugador (Premio_id_pre, Jugador_id_ju) "
                        f"VALUES ({id_pre}, {id_jugador});"
                    )
                else:
                    print(f"    ⚠️  Jugador no encontrado: '{nombre_jugador}'")
    
    # 💾 ESCRIBIR ARCHIVOS
    OUT_PREMIO.write_text(
        "-- 🏆 PREMIOS FIFA - Generados automáticamente (CON pais_pre)\n"
        + f"-- id_pre inicia en {next_id_pre-1} (ajusta seq_premio_id_pre START WITH {next_id_pre})\n\n"
        + "\n".join(inserts_premio) + "\n",
        encoding='utf-8'
    )
    
    OUT_PREMIOS_JUGADOR.write_text(
        "-- 🏆 PREMIOS FIFA - Jugadores ganadores\n"
        + "-- Requiere que se hayan insertado Premios primero\n\n"
        + "\n".join(inserts_premios_jugador) + "\n",
        encoding='utf-8'
    )
    
    print(f"\n✅ ¡LISTO!")
    print(f"📊 {len(inserts_premio)} INSERTs para Premio (incluye Fair Play)")
    print(f"📊 {len(inserts_premios_jugador)} INSERTs para Premios_Jugador")
    print(f"💾 Archivos:\n   {OUT_PREMIO}\n   {OUT_PREMIOS_JUGADOR}")

if __name__ == "__main__":
    generar_inserts_sql()
