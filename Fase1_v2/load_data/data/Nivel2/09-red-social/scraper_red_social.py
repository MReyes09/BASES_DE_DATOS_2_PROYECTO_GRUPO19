#!/usr/bin/env python3

import re
from pathlib import Path
from bs4 import BeautifulSoup
from multiprocessing import Pool
from difflib import SequenceMatcher
import time

HTML_DIR = Path(r"C:\Users\matth\Downloads\00-html")
JUGADOR_SQL = Path(r"C:\Users\matth\OneDrive\Escritorio\SEMESTRE\LAB_BASES_2\Proyectos\BASES_DE_DATOS_2_PROYECTO_GRUPO19\Fase1_v2\load_data\data\Nivel1\3jugador.sql")
OUTPUT_SQL = Path(__file__).parent / "9red_social_PERFECTO.sql"

def normalizar_basic(nombre):
    """Normaliza SIN quitar acentos para fuzzy matching"""
    return re.sub(r'\s+', ' ', nombre.replace("''", "'").strip().lower())

def quitar_acentos(nombre):
    """Quita acentos para comparación final"""
    return nombre.replace('á','a').replace('é','e').replace('í','i').replace('ó','o').replace('ú','u').replace('ñ','n')

def similarity(a, b):
    """Calcula similitud entre 2 strings (0-100%)"""
    return SequenceMatcher(None, a, b).ratio() * 100

def cargar_jugadores():
    mapa = {}
    pattern = re.compile(r"VALUES\s*\(\s*(\d+),\s*'([^']*(?:''[^']*)*)'", re.I)
    
    with open(JUGADOR_SQL, encoding="utf-8", errors="ignore") as f:
        for linea in f:
            if "INSERT INTO Jugador" not in linea: continue
            m = pattern.search(linea)
            if m:
                id_ju = int(m.group(1))
                nombre_norm = normalizar_basic(m.group(2))
                mapa[nombre_norm] = id_ju
    
    print(f"✅ {len(mapa)} jugadores cargados")
    return mapa

def encontrar_jugador(nombre_html, jugadores):
    """Encuentra el mejor match con fuzzy matching"""
    nombre_norm = normalizar_basic(nombre_html)
    nombre_sin_acento = quitar_acentos(nombre_norm)
    
    mejor_match = None
    mejor_score = 0
    
    for nombre_sql, id_ju in jugadores.items():
        # Comparación 1: directo
        score1 = similarity(nombre_norm, nombre_sql)
        if score1 > 95:  # Match perfecto
            return id_ju, nombre_sql, score1
        
        # Comparación 2: sin acentos
        nombre_sql_sin_acento = quitar_acentos(nombre_sql)
        score2 = similarity(nombre_sin_acento, nombre_sql_sin_acento)
        
        score = max(score1, score2)
        if score > mejor_score and score > 85:  # Umbral mínimo
            mejor_score = score
            mejor_match = (id_ju, nombre_sql, score)
    
    return mejor_match

def clasificar_red(url, texto):
    """🔥 Clasifica TODAS las redes sociales (incluido TikTok)"""
    url = url.lower()
    
    # TIKTOK
    if "tiktok.com" in url:
        user = url.split("tiktok.com/")[-1].split("/")[0].split("?")[0]
        if len(user) > 1:
            return "TikTok", "@" + user
    
    # INSTAGRAM
    if "instagram.com" in url:
        user = url.split("instagram.com/")[-1].split("/")[0].split("?")[0]
        return "Instagram", "@" + user
    
    # FACEBOOK
    if "facebook.com" in url or "fb.com" in url:
        user = url.split("facebook.com/")[-1].split("/")[0].split("?")[0]
        return "Facebook", "@" + user
    
    # TWITTER/X
    if "twitter.com" in url or "x.com" in url:
        user = url.split("twitter.com/")[-1].split("/")[0].split("?")[0]
        return "Twitter", "@" + user
    
    # YOUTUBE
    if "youtube.com" in url:
        return "YouTube", texto.strip()
    
    return None

def procesar_html(args):
    path, jugadores = args
    filename = Path(path).name
    
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            soup = BeautifulSoup(f.read(), 'lxml')
        
        # 1. NOMBRE HTML (PRIMERO nombre completo de la tabla)
        nombre_completo = None
        tabla = soup.find("table", class_="w-auto")
        if tabla:
            for tr in tabla.find_all("tr", class_="a-top"):
                tds = tr.find_all("td")
                if len(tds) >= 2:
                    b = tds[0].find("b")
                    if b and "nombre completo" in b.get_text().lower():
                        span = tds[1].find("span")
                        nombre_completo = span.get_text(strip=True) if span else tds[1].get_text(strip=True)
                        break
        
        # Fallback: h2.t-enc-1
        if not nombre_completo:
            h2 = soup.select_one("h2.t-enc-1")
            if h2:
                nombre_completo = h2.get_text(strip=True)
        
        if not nombre_completo:
            print(f"⚠️  {filename}: NO nombre encontrado")
            return []
        
        # 2. BUSCAR MATCH EN SQL
        match = encontrar_jugador(nombre_completo, jugadores)
        if not match:
            print(f"❌ {filename}: '{nombre_completo}' NO tiene match (>85%)")
            return []
        
        jugador_id, nombre_sql, score = match
        
        # 3. REDES SOCIALES
        redes_encontradas = []
        for b in soup.find_all("b"):
            if "redes sociales" in b.get_text(strip=True).lower():
                tr = b.find_parent("tr")
                if tr:
                    tds = tr.find_all("td")
                    if len(tds) >= 2:
                        td_links = tds[1]
                        for a in td_links.find_all("a", href=True):
                            data = clasificar_red(a["href"], a.get_text(strip=True))
                            if data:
                                tipo, usuario = data
                                redes_encontradas.append((tipo, usuario))
                        break
        
        # MOSTRAR RESULTADO
        redes_str = ", ".join([f"{t}:{u}" for t,u in redes_encontradas]) if redes_encontradas else "NINGUNA"
        status = "✅" if redes_encontradas else "➖"
        print(f"{status} {filename}: '{nombre_completo}' [{score:.0f}%] → ID:{jugador_id} - {redes_str}")
        
        # GENERAR INSERTS
        inserts = []
        for tipo, usuario in redes_encontradas:
            inserts.append({
                'id_red': 0,
                'usuario': usuario.replace("'", "''"),
                'tipo': tipo,
                'jugador_id': jugador_id,
                'filename': filename,
                'nombre_html': nombre_completo,
                'match_score': score
            })
        
        return inserts
        
    except Exception as e:
        print(f"💥 ERROR {filename}: {e}")
        return []

def main():
    print("🚀 SCRAPER REDES SOCIALES COMPLETO (TikTok + 4 CPUs)")
    print("=" * 80)
    
    jugadores = cargar_jugadores()
    html_files = list(HTML_DIR.glob("*.html"))
    print(f"📁 {len(html_files)} HTMLs encontrados")
    
    if not html_files:
        print("❌ No hay HTMLs!")
        return
    
    # Multiproceso 4 CPUs ⚡
    print("\n⚡ Iniciando 4 CPUs...")
    start_time = time.time()
    
    with Pool(processes=4) as pool:
        worker_args = [(path, jugadores) for path in html_files]
        todos_inserts = pool.map(procesar_html, worker_args)
    
    # Procesar resultados
    inserts_final = []
    for batch in todos_inserts:
        inserts_final.extend(batch)
    
    for i, insert in enumerate(inserts_final, 1):
        insert['id_red'] = i
    
    elapsed = time.time() - start_time
    print(f"\n⏱️  Tiempo: {elapsed:.1f}s")
    print(f"📊 Total INSERTs: {len(inserts_final)}")
    
    # Guardar SQL
    with open(OUTPUT_SQL, 'w', encoding='utf-8') as f:
        f.write("-- Redes sociales de jugadores (Instagram/Facebook/Twitter/YouTube/TikTok)\n")
        f.write(f"-- Total: {len(inserts_final)} inserts\n")
        f.write(f"-- Tiempo: {elapsed:.1f}s | 4 CPUs\n\n")
        
        for ins in inserts_final:
            sql = (f"INSERT INTO Red_social "
                   f"VALUES ({ins['id_red']}, '{ins['usuario']}', '{ins['tipo']}', {ins['jugador_id']});")
            f.write(sql + "\n")
    
    print(f"💾 Guardado: {OUTPUT_SQL}")
    print("🎉 ¡TikTok incluido! Listo para cargar en Oracle")

if __name__ == "__main__":
    main()
