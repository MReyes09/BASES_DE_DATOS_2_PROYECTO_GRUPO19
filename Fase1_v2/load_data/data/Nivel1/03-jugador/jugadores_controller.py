import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import re
import json
import random
import unicodedata
from dotenv import load_dotenv
from typing import List, Dict, Any, Optional

try:
    import cloudscraper
except ImportError:
    cloudscraper = None

load_dotenv()

FIELD_MAP = {
    'Nombre completo': 'nombre_completo',
    'Fecha de Nacimiento': 'fecha_nacimiento',
    'Lugar de nacimiento': 'lugar_nacimiento',
    'Posición': 'posicion',
    'Números de camiseta': 'numeros_camiseta',
    'Altura': 'altura',
    'Apodo': 'apodo',
    'Sitio Web Oficial': 'sitio_web',
    'Redes Sociales': 'redes_sociales',
}


class JugadoresController:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'https://www.losmundialesdefutbol.com')
        self.headers = {
            'User-Agent': os.getenv('USER_AGENT',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
            'Referer': self.base_url,
            'Connection': 'keep-alive',
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.trust_env = True
        self.cloudscraper = None

        # Proxy: configurar via .env o variable de entorno
        # Ejemplos:
        #   PROXY=http://127.0.0.1:8080
        #   PROXY=socks5://127.0.0.1:1080
        proxy = os.getenv('PROXY', '')
        if proxy:
            self.session.proxies = {
                'http': proxy,
                'https': proxy,
            }
            print(f"🔒 Usando proxy: {proxy}")

        use_cloudscraper = os.getenv('USE_CLOUDSCRAPER', '1') == '1'
        if use_cloudscraper and cloudscraper is not None:
            self.cloudscraper = cloudscraper.create_scraper(
                browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False}
            )
            self.cloudscraper.headers.update(self.headers)
            if proxy:
                self.cloudscraper.proxies = {
                    'http': proxy,
                    'https': proxy,
                }

        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
        student_id = os.getenv('JUGADORES_STUDENT_ID', '202300512')
        output_dir = os.getenv('JUGADORES_OUTPUT_DIR', '')

        if output_dir:
            if not os.path.isabs(output_dir):
                output_dir = os.path.join(project_root, output_dir)
            self.data_dir = os.path.abspath(output_dir)
        else:
            self.data_dir = os.path.join(project_root, 'data', student_id, 'Jugadores')

        self.cache_dir = os.path.join(self.data_dir, 'cache')
        self.progress_file = os.path.join(self.data_dir, 'progress.json')

        # Directorio de HTMLs descargados manualmente (fallback offline)
        self.local_html_dirs: List[str] = []
        local_html = os.getenv('JUGADORES_LOCAL_HTML', '')
        if local_html:
            for d in local_html.split(';'):
                d = d.strip()
                if d and not os.path.isabs(d):
                    d = os.path.join(project_root, d)
                if d and os.path.isdir(d):
                    self.local_html_dirs.append(os.path.abspath(d))
        # Auto-detectar carpeta Apodo del mismo estudiante
        apodo_dir = os.path.join(project_root, 'data', student_id, 'Apodo')
        if os.path.isdir(apodo_dir) and apodo_dir not in self.local_html_dirs:
            self.local_html_dirs.append(apodo_dir)
        # Auto-detectar carpeta 00-html (descargas de Selenium)
        html_dir = os.path.join(project_root, 'data', student_id, '00-html')
        if os.path.isdir(html_dir) and html_dir not in self.local_html_dirs:
            self.local_html_dirs.append(html_dir)
        # Auto-detectar carpeta temp
        temp_dir = os.path.join(project_root, 'data', student_id, 'temp')
        if os.path.isdir(temp_dir) and temp_dir not in self.local_html_dirs:
            self.local_html_dirs.append(temp_dir)
        if self.local_html_dirs:
            print(f"📂 Directorios HTML locales: {self.local_html_dirs}")

        self.delay_min = 2
        self.delay_max = 5
        self.max_retries = int(os.getenv('JUGADORES_RETRIES', '2'))
        self.retry_wait_base = int(os.getenv('JUGADORES_RETRY_WAIT_BASE', '3'))
        self.retry_wait_cap = int(os.getenv('JUGADORES_RETRY_WAIT_CAP', '15'))
        self.request_timeout = int(os.getenv('JUGADORES_TIMEOUT', '20'))

    # =========================================================================
    # Progreso y cache
    # =========================================================================

    def _load_progress(self) -> Dict:
        if os.path.exists(self.progress_file):
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {'countries_done': [], 'players_done': []}

    def _save_progress(self, progress: Dict):
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, ensure_ascii=False, indent=2)

    def _find_local_html(self, url: str) -> Optional[str]:
        """Busca un HTML descargado manualmente que corresponda a la URL."""
        # Extraer slug de la URL para busqueda por nombre de archivo
        slug_match = re.search(r'/jugadores/(\w+)\.php', url)
        url_slug = slug_match.group(1) if slug_match else None

        for d in self.local_html_dirs:
            for fname in os.listdir(d):
                if not fname.endswith('.html'):
                    continue

                # Match directo por nombre de archivo (ej: lionel_messi.html)
                if url_slug and fname == f"{url_slug}.html":
                    return os.path.join(d, fname)

                fpath = os.path.join(d, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        head = f.read(2048)
                    # Formato: <!-- saved from url=(NNNN)https://... -->
                    m = re.search(r'saved from url=\(\d+\)(\S+)', head)
                    if m and m.group(1).rstrip('/') == url.rstrip('/'):
                        return fpath
                except Exception:
                    continue
        return None

    def _cache_path(self, url: str) -> str:
        slug = url.replace(self.base_url, '').strip('/')
        slug = slug.replace('/', '_').replace('.php', '.html')
        return os.path.join(self.cache_dir, slug)

    def _fetch_with_cache(self, url: str, retries: Optional[int] = None) -> str:
        retries = retries or self.max_retries
        cached = self._cache_path(url)
        if os.path.exists(cached):
            with open(cached, 'r', encoding='utf-8') as f:
                cached_html = f.read()
                if cached_html.strip():
                    return cached_html

        # Buscar en HTMLs descargados manualmente
        local_path = self._find_local_html(url)
        if local_path:
            print(f"  📄 Usando HTML local: {os.path.basename(local_path)}")
            with open(local_path, 'r', encoding='utf-8') as f:
                html = f.read()
            # Guardar en cache para futuras llamadas
            os.makedirs(os.path.dirname(cached), exist_ok=True)
            with open(cached, 'w', encoding='utf-8') as f:
                f.write(html)
            return html

        status_history = []
        last_error = ''
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=self.request_timeout)
                status_history.append(str(response.status_code))

                if response.status_code == 429 or response.status_code == 403:
                    retry_after = response.headers.get('Retry-After')
                    if retry_after and retry_after.isdigit():
                        wait = int(retry_after)
                    else:
                        wait = min(self.retry_wait_cap, self.retry_wait_base * (attempt + 1))

                    print(f"  ⚠️ {response.status_code} en {url} - esperando {wait}s...")
                    if attempt < retries - 1:
                        time.sleep(wait)
                    continue

                response.raise_for_status()
                html = response.text
                if not html.strip():
                    raise requests.HTTPError(f"Respuesta vacía para {url}")

                os.makedirs(os.path.dirname(cached), exist_ok=True)
                with open(cached, 'w', encoding='utf-8') as f:
                    f.write(html)

                time.sleep(random.uniform(self.delay_min, self.delay_max))
                return html

            except requests.RequestException as e:
                last_error = str(e)
                if attempt < retries - 1:
                    wait = 5 * (attempt + 1)
                    print(f"  ⚠️ Error en {url}: {e} - reintentando en {wait}s...")
                    time.sleep(wait)
                else:
                    break

        if self.cloudscraper is not None and status_history and all(s == '403' for s in status_history):
            try:
                print(f"  🔁 Probando cloudscraper para {url}...")
                response = self.cloudscraper.get(url, timeout=self.request_timeout)
                status_history.append(f"cs:{response.status_code}")
                response.raise_for_status()

                html = response.text
                if not html.strip():
                    raise RuntimeError(f"Respuesta vacia con cloudscraper para {url}")

                os.makedirs(os.path.dirname(cached), exist_ok=True)
                with open(cached, 'w', encoding='utf-8') as f:
                    f.write(html)

                return html
            except Exception as e:
                last_error = str(e)

        estados = ','.join(status_history) if status_history else 'sin respuesta'
        raise RuntimeError(
            f"No se pudo obtener {url} tras {retries} intentos. "
            f"Estados: {estados}. Ultimo error: {last_error or 'N/A'}"
        )

    def _log_error(self, player_slug: str, error: str):
        os.makedirs(self.data_dir, exist_ok=True)
        with open(os.path.join(self.data_dir, 'errors.log'), 'a', encoding='utf-8') as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} | {player_slug} | {error}\n")

    def _normalizar_texto(self, texto: str) -> str:
        texto = texto.lower().strip().replace('-', ' ').replace('_', ' ')
        return ''.join(
            c for c in unicodedata.normalize('NFKD', texto)
            if not unicodedata.combining(c)
        )

    def _resolver_country_slug(self, country_slug: str) -> str:
        objetivo = self._normalizar_texto(country_slug)
        paises = self._extraer_paises_con_slugs()

        for pais in paises:
            if objetivo == self._normalizar_texto(pais['slug']):
                return pais['slug']
            if objetivo == self._normalizar_texto(pais['nombre_pais']):
                return pais['slug']

        raise ValueError(f"No se encontró un país para '{country_slug}'. Usa /api/jugadores/countries para ver slugs válidos.")

    # =========================================================================
    # CSV incremental
    # =========================================================================

    def _append_to_csv(self, filename: str, headers: List[str], rows: List[List]):
        filepath = os.path.join(self.data_dir, filename)
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
        with open(filepath, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if not file_exists:
                writer.writerow(headers)
            writer.writerows(rows)

    # =========================================================================
    # Fase 1: Extraer paises con slugs
    # =========================================================================

    def _extraer_paises_con_slugs(self) -> List[Dict[str, str]]:
        url = f"{self.base_url}/jugadores.php"
        html = self._fetch_with_cache(url)
        soup = BeautifulSoup(html, 'html.parser')

        paises = []
        seen = set()

        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            match = re.search(r'jugadores_indice/(\w+)\.php', href)
            if match:
                slug = match.group(1)
                if slug not in seen:
                    seen.add(slug)
                    nombre = a_tag.get_text(strip=True)
                    if not nombre:
                        img = a_tag.find('img')
                        nombre = img['alt'] if img and img.get('alt') else slug
                    paises.append({
                        'nombre_pais': nombre,
                        'slug': slug,
                    })

        print(f"✅ {len(paises)} países encontrados")
        return paises

    # =========================================================================
    # Fase 2: Extraer jugadores de un pais
    # =========================================================================

    def _extraer_jugadores_de_pais(self, country_slug: str) -> List[Dict[str, str]]:
        url = f"{self.base_url}/jugadores_indice/{country_slug}.php"
        html = self._fetch_with_cache(url)
        soup = BeautifulSoup(html, 'html.parser')

        jugadores = []
        for div in soup.find_all('div', class_='margen-b3'):
            a_tag = div.find('a', href=True)
            if a_tag and '/jugadores/' in a_tag['href']:
                match = re.search(r'jugadores/(\w+)\.php', a_tag['href'])
                if match:
                    jugadores.append({
                        'nombre_display': a_tag.get_text(strip=True),
                        'slug': match.group(1),
                    })

        return jugadores

    # =========================================================================
    # Fase 3: Extraer detalle de un jugador
    # =========================================================================

    def _extraer_seleccion_nacional(self, soup: BeautifulSoup) -> str:
        """Extrae el país de la sección 'Seleccion Nacional' del HTML del jugador."""
        # Buscar h3 que contenga "Seleccion Nacional"
        for h3 in soup.find_all('h3'):
            text = h3.get_text(strip=True).lower()
            if 'seleccion nacional' in text or 'selección nacional' in text:
                # El link con el pais esta en el siguiente <p> o <a> hermano
                parent = h3.find_parent('div')
                if parent:
                    a_tag = parent.find('a', href=re.compile(r'selecciones/\w+'))
                    if a_tag:
                        # El texto puede tener saltos, tomar la ultima parte limpia
                        country = a_tag.get_text(strip=True)
                        if country:
                            return country
                        # Fallback: alt del img dentro del link
                        img = a_tag.find('img')
                        if img and img.get('alt'):
                            return img['alt']
        return ''

    def _extraer_detalle_jugador(self, player_slug: str, country_name: str) -> Dict[str, Any]:
        url = f"{self.base_url}/jugadores/{player_slug}.php"
        html = self._fetch_with_cache(url)
        soup = BeautifulSoup(html, 'html.parser')

        # Nombre display desde h2
        h2 = soup.find('h2', class_='t-enc-1')
        nombre_display = h2.get_text(strip=True) if h2 else player_slug

        # Extraer pais desde la seccion "Seleccion Nacional" del HTML
        seleccion = self._extraer_seleccion_nacional(soup)
        if seleccion:
            country_name = seleccion

        # Info table
        info = self._parse_info_table(soup)

        # Estadisticas
        estadisticas = self._extraer_estadisticas(soup)

        # Detalle por mundiales
        mundiales_detalle = self._extraer_detalle_mundiales(soup)

        # Redes sociales (extraer aparte si existen)
        redes = info.pop('redes_sociales', [])

        return {
            'slug': player_slug,
            'nombre_display': nombre_display,
            'pais': country_name,
            'info': info,
            'redes': redes,
            'estadisticas': estadisticas,
            'mundiales_detalle': mundiales_detalle,
        }

    def _parse_info_table(self, soup: BeautifulSoup) -> Dict[str, Any]:
        info = {}
        table = soup.find('table', class_='w-auto')
        if not table:
            return info

        for row in table.find_all('tr', class_='a-top'):
            tds = row.find_all('td')
            if len(tds) < 2:
                continue

            label_tag = tds[0].find('b')
            if not label_tag:
                continue

            label = label_tag.get_text(strip=True).rstrip(':')
            value_td = tds[1]

            if label == 'Nombre completo':
                span = value_td.find('span')
                info['nombre_completo'] = span.get_text(strip=True) if span else value_td.get_text(strip=True)

            elif label == 'Sitio Web Oficial':
                a_tag = value_td.find('a')
                info['sitio_web'] = a_tag['href'] if a_tag else value_td.get_text(strip=True)

            elif label == 'Redes Sociales':
                info['redes_sociales'] = self._parse_redes_sociales(value_td)

            elif label == 'Apodo':
                info['apodo'] = value_td.get_text(strip=True)

            else:
                key = FIELD_MAP.get(label)
                if key:
                    info[key] = value_td.get_text(strip=True)
                else:
                    info[label.lower().replace(' ', '_').replace('á', 'a').replace('é', 'e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')] = value_td.get_text(strip=True)

        return info

    def _parse_redes_sociales(self, td) -> List[Dict[str, str]]:
        redes = []
        # Buscar spans con clase d-inline-block
        spans = td.find_all('span', class_='d-inline-block')
        for span in spans:
            a_tag = span.find('a')
            if a_tag:
                text = span.get_text(strip=True)
                parts = text.split(':', 1)
                platform = parts[0].strip() if len(parts) > 1 else 'Otro'
                handle = a_tag.get_text(strip=True)
                url = a_tag.get('href', '')
                redes.append({
                    'platform': platform,
                    'url': url,
                    'handle': handle,
                })

        # Fallback: si no hay spans con esa clase, buscar todos los <a> directamente
        if not redes:
            for a_tag in td.find_all('a', href=True):
                href = a_tag['href']
                handle = a_tag.get_text(strip=True)
                platform = 'Otro'
                if 'instagram' in href.lower():
                    platform = 'Instagram'
                elif 'facebook' in href.lower():
                    platform = 'Facebook'
                elif 'youtube' in href.lower():
                    platform = 'YouTube'
                elif 'twitter' in href.lower() or 'x.com' in href.lower():
                    platform = 'X/Twitter'
                redes.append({
                    'platform': platform,
                    'url': href,
                    'handle': handle,
                })

        return redes

    def _extraer_estadisticas(self, soup: BeautifulSoup) -> Dict[str, Any]:
        stats = {
            'mundiales': 0,
            'partidos': 0,
            'goles': 0,
            'promedio_gol': 0.0,
            'campeon': '-',
        }

        # Buscar la seccion de estadisticas
        h3_tags = soup.find_all('h3')
        stats_section = None
        for h3 in h3_tags:
            if 'Estadísticas' in h3.get_text() or 'Estadisticas' in h3.get_text():
                stats_section = h3.find_parent('div', class_='margen-y15')
                break

        if not stats_section:
            return stats

        # Primera tabla (mundiales, partidos, campeon)
        div_60 = stats_section.find('div', class_='rd-100-60')
        if div_60:
            data_row = div_60.find('tr', class_='a-center')
            if data_row:
                tds = data_row.find_all('td')
                if len(tds) >= 1:
                    text = tds[0].get_text(strip=True)
                    nums = re.findall(r'\d+', text)
                    if nums:
                        stats['mundiales'] = int(nums[0])
                if len(tds) >= 2:
                    text = tds[1].get_text(strip=True)
                    nums = re.findall(r'\d+', text)
                    if nums:
                        stats['partidos'] = int(nums[0])
                if len(tds) >= 3:
                    a_tag = tds[2].find('a')
                    if a_tag:
                        stats['campeon'] = a_tag.get_text(strip=True)
                    else:
                        stats['campeon'] = '-'

        # Segunda tabla (goles, promedio)
        div_40 = stats_section.find('div', class_='rd-100-40')
        if div_40:
            data_row = div_40.find('tr', class_='a-center')
            if data_row:
                tds = data_row.find_all('td')
                if len(tds) >= 1:
                    text = tds[0].get_text(strip=True)
                    nums = re.findall(r'\d+', text)
                    if nums:
                        stats['goles'] = int(nums[0])
                if len(tds) >= 2:
                    text = tds[1].get_text(strip=True)
                    nums = re.findall(r'[\d.]+', text)
                    if nums:
                        try:
                            stats['promedio_gol'] = float(nums[0])
                        except ValueError:
                            pass

        return stats

    def _extraer_detalle_mundiales(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        detalles = []

        # Buscar la seccion "Detalle de Mundiales Jugados"
        h3_tags = soup.find_all('h3')
        detail_section = None
        for h3 in h3_tags:
            if 'Detalle de Mundiales' in h3.get_text():
                detail_section = h3.find_parent('div', class_='margen-y15')
                break

        if not detail_section:
            return detalles

        table = detail_section.find('table', class_='a-center')
        if not table:
            return detalles

        rows = table.find_all('tr')

        for row in rows:
            # Saltar headers y totales
            if row.find('td', class_='t-enc-4') or row.find('td', class_='t-enc-5'):
                continue
            classes = row.get('class', [])
            if 't-enc-4' in classes or 't-enc-5' in classes:
                continue
            if row.find('strong') and 'Totales' in row.get_text():
                continue

            tds = row.find_all('td')
            if len(tds) < 10:
                continue

            # Extraer mundial (año)
            mundial_td = tds[0]
            a_tag = mundial_td.find('a')
            mundial = a_tag.get_text(strip=True) if a_tag else mundial_td.get_text(strip=True)

            # Filtrar si no es un año valido
            if not re.match(r'\d{4}', mundial.strip()):
                continue

            def get_td_text(idx):
                return tds[idx].get_text(strip=True) if idx < len(tds) else ''

            detalle = {
                'mundial': mundial.strip(),
                'camiseta': get_td_text(1),
                'posicion': get_td_text(2),
                'jugo': get_td_text(3),
                'titular': get_td_text(4),
                'capitan': get_td_text(5),
                'no_jugo': get_td_text(6),
                'goles': get_td_text(7),
                'prom_gol': get_td_text(8),
                'ta': get_td_text(9),
                'tr': get_td_text(10),
                'pg': get_td_text(11),
                'pe': get_td_text(12),
                'pp': get_td_text(13),
                'pos_final': get_td_text(14),
            }
            detalles.append(detalle)

        return detalles

    # =========================================================================
    # Orquestador principal
    # =========================================================================

    def scrape_all_players(self) -> Dict[str, Any]:
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        progress = self._load_progress()

        # Fase 1: Paises
        paises = self._extraer_paises_con_slugs()
        total_jugadores = 0
        errores = 0

        for i_pais, pais in enumerate(paises, 1):
            if pais['slug'] in progress['countries_done']:
                print(f"⏭️  [{i_pais}/{len(paises)}] {pais['nombre_pais']} (ya procesado)")
                continue

            print(f"\n🌍 [{i_pais}/{len(paises)}] {pais['nombre_pais']}...")

            # Fase 2: Jugadores del pais
            try:
                jugadores = self._extraer_jugadores_de_pais(pais['slug'])
            except Exception as e:
                print(f"  ❌ Error obteniendo jugadores: {e}")
                self._log_error(pais['slug'], f"Error listado: {e}")
                continue

            print(f"  📋 {len(jugadores)} jugadores encontrados")

            for i_jug, jugador in enumerate(jugadores, 1):
                if jugador['slug'] in progress['players_done']:
                    continue

                print(f"  👤 [{i_jug}/{len(jugadores)}] {jugador['nombre_display']}...", end=' ')

                try:
                    detalle = self._extraer_detalle_jugador(jugador['slug'], pais['nombre_pais'])
                    self._guardar_jugador_csv(detalle)
                    progress['players_done'].append(jugador['slug'])
                    total_jugadores += 1
                    print("✅")
                except Exception as e:
                    errores += 1
                    print(f"❌ {e}")
                    self._log_error(jugador['slug'], str(e))

                # Guardar progreso cada 10 jugadores
                if total_jugadores % 10 == 0:
                    self._save_progress(progress)

            progress['countries_done'].append(pais['slug'])
            self._save_progress(progress)
            print(f"  ✅ {pais['nombre_pais']} completado")

        self._save_progress(progress)
        print(f"\n🏁 COMPLETADO: {total_jugadores} jugadores, {errores} errores")

        return {
            'success': True,
            'total_jugadores': total_jugadores,
            'total_errores': errores,
            'total_paises': len(paises),
        }

    def scrape_single_country(self, country_slug: str) -> Dict[str, Any]:
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)

        resolved_country_slug = self._resolver_country_slug(country_slug)
        jugadores = self._extraer_jugadores_de_pais(resolved_country_slug)
        total = 0
        errores = 0

        for i, jugador in enumerate(jugadores, 1):
            print(f"  👤 [{i}/{len(jugadores)}] {jugador['nombre_display']}...", end=' ')
            try:
                detalle = self._extraer_detalle_jugador(jugador['slug'], resolved_country_slug)
                self._guardar_jugador_csv(detalle)
                total += 1
                print("✅")
            except Exception as e:
                errores += 1
                print(f"❌ {e}")
                self._log_error(jugador['slug'], str(e))

        return {
            'success': True,
            'country_requested': country_slug,
            'country_resolved': resolved_country_slug,
            'total_jugadores': total,
            'total_errores': errores,
        }

    def scrape_single_player(self, player_slug: str, country: str = 'Desconocido') -> Dict[str, Any]:
        os.makedirs(self.data_dir, exist_ok=True)
        os.makedirs(self.cache_dir, exist_ok=True)
        detalle = self._extraer_detalle_jugador(player_slug, country)
        self._guardar_jugador_csv(detalle)
        return detalle

    # =========================================================================
    # Escritura a CSV
    # =========================================================================

    def _guardar_jugador_csv(self, detalle: Dict[str, Any]):
        info = detalle['info']
        slug = detalle['slug']
        nombre = detalle['nombre_display']
        pais = detalle['pais']

        # 1. jugadores.csv
        self._append_to_csv('jugadores.csv',
            ['player_slug', 'nombre_display', 'nombre_completo', 'fecha_nacimiento',
             'lugar_nacimiento', 'posicion', 'numeros_camiseta', 'altura', 'pais', 'sitio_web'],
            [[
                slug, nombre,
                info.get('nombre_completo', ''),
                info.get('fecha_nacimiento', ''),
                info.get('lugar_nacimiento', ''),
                info.get('posicion', ''),
                info.get('numeros_camiseta', ''),
                info.get('altura', ''),
                pais,
                info.get('sitio_web', ''),
            ]]
        )

        # 2. jugadores_apodos.csv
        apodo = info.get('apodo', '')
        if apodo:
            self._append_to_csv('jugadores_apodos.csv',
                ['player_slug', 'nombre_display', 'apodo'],
                [[slug, nombre, apodo]]
            )

        # 3. jugadores_redes.csv
        for red in detalle.get('redes', []):
            self._append_to_csv('jugadores_redes.csv',
                ['player_slug', 'nombre_display', 'platform', 'url', 'handle'],
                [[slug, nombre, red['platform'], red['url'], red['handle']]]
            )

        # 4. jugadores_estadisticas.csv
        stats = detalle.get('estadisticas', {})
        self._append_to_csv('jugadores_estadisticas.csv',
            ['player_slug', 'nombre_display', 'pais', 'mundiales', 'partidos',
             'goles', 'promedio_gol', 'campeon'],
            [[
                slug, nombre, pais,
                stats.get('mundiales', 0),
                stats.get('partidos', 0),
                stats.get('goles', 0),
                stats.get('promedio_gol', 0.0),
                stats.get('campeon', '-'),
            ]]
        )

        # 5. jugadores_mundiales_detalle.csv
        for md in detalle.get('mundiales_detalle', []):
            self._append_to_csv('jugadores_mundiales_detalle.csv',
                ['player_slug', 'nombre_display', 'mundial', 'camiseta', 'posicion',
                 'jugo', 'titular', 'capitan', 'no_jugo', 'goles', 'prom_gol',
                 'ta', 'tr', 'pg', 'pe', 'pp', 'pos_final'],
                [[
                    slug, nombre,
                    md.get('mundial', ''),
                    md.get('camiseta', ''),
                    md.get('posicion', ''),
                    md.get('jugo', ''),
                    md.get('titular', ''),
                    md.get('capitan', ''),
                    md.get('no_jugo', ''),
                    md.get('goles', ''),
                    md.get('prom_gol', ''),
                    md.get('ta', ''),
                    md.get('tr', ''),
                    md.get('pg', ''),
                    md.get('pe', ''),
                    md.get('pp', ''),
                    md.get('pos_final', ''),
                ]]
            )

    def scrape_local_html_dir(self, directory: Optional[str] = None) -> Dict[str, Any]:
        """Procesa todos los archivos HTML de jugadores en un directorio local."""
        os.makedirs(self.data_dir, exist_ok=True)

        dirs_to_scan = [directory] if directory else self.local_html_dirs
        total = 0
        errores = 0
        processed = []

        for d in dirs_to_scan:
            if not os.path.isdir(d):
                continue
            for fname in os.listdir(d):
                if not fname.endswith('.html'):
                    continue
                fpath = os.path.join(d, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        html = f.read()

                    # Extraer URL original para determinar tipo de pagina
                    m = re.search(r'saved from url=\(\d+\)(\S+)', html[:2048])
                    if not m:
                        continue
                    url = m.group(1)

                    # Solo procesar paginas de jugadores individuales
                    slug_match = re.search(r'/jugadores/(\w+)\.php', url)
                    if not slug_match:
                        continue

                    player_slug = slug_match.group(1)
                    print(f"  📄 Procesando {fname} -> {player_slug}...", end=' ')

                    soup = BeautifulSoup(html, 'html.parser')

                    # Determinar pais desde la seccion "Seleccion Nacional"
                    country = self._extraer_seleccion_nacional(soup) or 'Desconocido'

                    h2 = soup.find('h2', class_='t-enc-1')
                    nombre_display = h2.get_text(strip=True) if h2 else player_slug
                    info = self._parse_info_table(soup)
                    estadisticas = self._extraer_estadisticas(soup)
                    mundiales_detalle = self._extraer_detalle_mundiales(soup)
                    redes = info.pop('redes_sociales', [])

                    detalle = {
                        'slug': player_slug,
                        'nombre_display': nombre_display,
                        'pais': country,
                        'info': info,
                        'redes': redes,
                        'estadisticas': estadisticas,
                        'mundiales_detalle': mundiales_detalle,
                    }

                    self._guardar_jugador_csv(detalle)
                    total += 1
                    processed.append(player_slug)
                    print("✅")

                except Exception as e:
                    errores += 1
                    print(f"❌ {e}")
                    self._log_error(fname, str(e))

        return {
            'success': True,
            'total_jugadores': total,
            'total_errores': errores,
            'jugadores': processed,
        }

    def get_countries(self) -> List[Dict[str, str]]:
        os.makedirs(self.cache_dir, exist_ok=True)
        return self._extraer_paises_con_slugs()

    def get_country_players(self, country_slug: str) -> List[Dict[str, str]]:
        os.makedirs(self.cache_dir, exist_ok=True)
        resolved_country_slug = self._resolver_country_slug(country_slug)
        return self._extraer_jugadores_de_pais(resolved_country_slug)
