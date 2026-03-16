"""
Script para procesar archivos HTML locales de jugadores y generar INSERTs SQL.
Lee de la carpeta 00-html y genera archivos SQL en data-jugadores.
"""

import os
import re
from bs4 import BeautifulSoup
from typing import List, Dict, Any, Optional
from datetime import datetime


class JugadoresLocalProcessor:
    def __init__(self):
        # Rutas base
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(os.path.join(script_dir, '..', '..'))

        # Carpeta de HTMLs descargados
        self.html_dir = os.path.join(project_root, 'Fase1', 'data', '202300512', '00-html')

        # Carpeta de salida para SQLs
        self.output_dir = os.path.join(script_dir, 'data-jugadores')
        os.makedirs(self.output_dir, exist_ok=True)

        # Contador de IDs
        self.jugador_id_counter = 1

        # Cache de jugadores procesados
        self.jugadores_procesados = {}

        # Mapeo de meses en español a números
        self.meses = {
            'enero': '01', 'febrero': '02', 'marzo': '03', 'abril': '04',
            'mayo': '05', 'junio': '06', 'julio': '07', 'agosto': '08',
            'septiembre': '09', 'octubre': '10', 'noviembre': '11', 'diciembre': '12'
        }

    def _parse_fecha_nacimiento(self, fecha_str: str) -> Optional[str]:
        """Convierte fecha en español a formato Oracle DATE."""
        if not fecha_str:
            return None

        # Formato esperado: "24 de junio de 1987"
        match = re.match(r'(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})', fecha_str.lower())
        if match:
            dia = match.group(1).zfill(2)
            mes_nombre = match.group(2)
            anio = match.group(3)
            mes = self.meses.get(mes_nombre)
            if mes:
                return f"TO_DATE('{dia}/{mes}/{anio}', 'DD/MM/YYYY')"
        return None

    def _escape_sql(self, value: str) -> str:
        """Escapa comillas simples para SQL."""
        if value is None:
            return 'NULL'
        return value.replace("'", "''")

    def _truncate(self, value: str, max_len: int) -> str:
        """Trunca un string al largo máximo."""
        if value and len(value) > max_len:
            return value[:max_len]
        return value

    def _extraer_slugs_de_indice(self) -> List[str]:
        """Lee los archivos _index_letra_X.html y extrae los slugs de jugadores."""
        slugs = []

        for letra in 'abcdefghijklmnopqrstuvwxyz':
            index_file = os.path.join(self.html_dir, f'_index_letra_{letra}.html')
            if not os.path.exists(index_file):
                print(f"  No encontrado: {index_file}")
                continue

            try:
                with open(index_file, 'r', encoding='utf-8') as f:
                    html = f.read()

                soup = BeautifulSoup(html, 'html.parser')

                # Buscar todos los links a jugadores
                for a_tag in soup.find_all('a', href=True):
                    href = a_tag['href']
                    match = re.search(r'jugadores/(\w+)\.php', href)
                    if match:
                        slug = match.group(1)
                        if slug not in slugs:
                            slugs.append(slug)

            except Exception as e:
                print(f"  Error leyendo {index_file}: {e}")

        return slugs

    def _extraer_info_jugador(self, html: str) -> Dict[str, Any]:
        """Extrae información de un jugador desde su HTML."""
        soup = BeautifulSoup(html, 'html.parser')
        info = {}

        # Nombre display desde h2 o title
        h2 = soup.find('h2', class_='t-enc-1')
        if h2:
            info['nombre_display'] = h2.get_text(strip=True)
        else:
            title = soup.find('title')
            if title:
                match = re.match(r'^(.+?)\s+en los Mundiales', title.get_text())
                if match:
                    info['nombre_display'] = match.group(1).strip()

        # Buscar tabla de información
        table = soup.find('table', class_='w-auto')
        if table:
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

                elif label == 'Fecha de Nacimiento':
                    info['fecha_nacimiento'] = value_td.get_text(strip=True)

                elif label == 'Lugar de nacimiento':
                    info['lugar_nacimiento'] = value_td.get_text(strip=True)

                elif label == 'Altura':
                    info['altura'] = value_td.get_text(strip=True)

                elif label == 'Apodo':
                    info['apodo'] = value_td.get_text(strip=True)

                elif label == 'Sitio Web Oficial':
                    a_tag = value_td.find('a')
                    info['sitio_web'] = a_tag['href'] if a_tag and a_tag.get('href') else value_td.get_text(strip=True)

                elif label == 'Posición':
                    info['posicion'] = value_td.get_text(strip=True)

                elif label == 'Números de camiseta':
                    info['numeros_camiseta'] = value_td.get_text(strip=True)

        # Extraer selecciones nacionales
        info['selecciones'] = self._extraer_selecciones(soup)

        # Extraer detalle de mundiales
        info['mundiales_detalle'] = self._extraer_detalle_mundiales(soup)

        return info

    def _extraer_selecciones(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """Extrae las selecciones nacionales del jugador."""
        selecciones = []

        # Buscar la sección "Selección Nacional" o "Selecciones Nacionales"
        for h3 in soup.find_all('h3'):
            text = h3.get_text(strip=True).lower()
            if 'seleccion nacional' in text or 'selección nacional' in text:
                parent = h3.find_parent('div', class_='rd-100-30')
                if parent:
                    for p in parent.find_all('p', class_='margen-b5'):
                        a_tag = p.find('a', href=re.compile(r'selecciones/\w+'))
                        if a_tag:
                            pais = a_tag.get_text(strip=True)
                            img = a_tag.find('img')
                            if not pais and img and img.get('alt'):
                                pais = img['alt']
                            if pais:
                                # Extraer slug del país
                                href_match = re.search(r'selecciones/(\w+)_seleccion', a_tag['href'])
                                slug = href_match.group(1) if href_match else ''
                                selecciones.append({
                                    'nombre': pais,
                                    'slug': slug
                                })

        # Si no encontró en esa estructura, buscar alternativa
        if not selecciones:
            for a_tag in soup.find_all('a', href=re.compile(r'selecciones/\w+_seleccion')):
                parent_div = a_tag.find_parent('div', class_='rd-100-30')
                if parent_div:
                    pais = a_tag.get_text(strip=True)
                    img = a_tag.find('img')
                    if not pais and img and img.get('alt'):
                        pais = img['alt']
                    if pais and pais not in [s['nombre'] for s in selecciones]:
                        href_match = re.search(r'selecciones/(\w+)_seleccion', a_tag['href'])
                        slug = href_match.group(1) if href_match else ''
                        selecciones.append({
                            'nombre': pais,
                            'slug': slug
                        })

        return selecciones

    def _extraer_detalle_mundiales(self, soup: BeautifulSoup) -> List[Dict[str, Any]]:
        """Extrae el detalle de mundiales jugados."""
        detalles = []

        # Buscar la sección "Detalle de Mundiales Jugados"
        for h3 in soup.find_all('h3'):
            if 'Detalle de Mundiales' in h3.get_text():
                detail_section = h3.find_parent('div', class_='margen-y15')
                if detail_section:
                    table = detail_section.find('table', class_='a-center')
                    if table:
                        rows = table.find_all('tr')
                        for row in rows:
                            # Saltar headers y totales
                            if row.find('td', class_='t-enc-4') or row.find('td', class_='t-enc-5'):
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

                            if not re.match(r'\d{4}', mundial.strip()):
                                continue

                            # Extraer país de la camiseta (segundo td)
                            camiseta_td = tds[1]
                            img = camiseta_td.find('img')
                            pais_mundial = img['alt'] if img and img.get('alt') else ''

                            # Extraer número de camiseta
                            camiseta_text = camiseta_td.get_text(strip=True)
                            num_match = re.search(r'(\d+)', camiseta_text)
                            numero_camiseta = int(num_match.group(1)) if num_match else None

                            def get_td_text(idx):
                                return tds[idx].get_text(strip=True) if idx < len(tds) else ''

                            def parse_int(val):
                                try:
                                    return int(val) if val else 0
                                except:
                                    return 0

                            detalle = {
                                'mundial': mundial.strip(),
                                'pais': pais_mundial,
                                'numero_camiseta': numero_camiseta,
                                'posicion': get_td_text(2),
                                'jugo': parse_int(get_td_text(3)),
                                'titular': parse_int(get_td_text(4)),
                                'capitan': parse_int(get_td_text(5)),
                                'no_jugo': parse_int(get_td_text(6)),
                                'goles': parse_int(get_td_text(7)),
                            }
                            detalles.append(detalle)
                break

        return detalles

    def process_all(self):
        """Procesa todos los jugadores y genera los archivos SQL."""
        print("=" * 60)
        print("PROCESADOR DE JUGADORES - HTML LOCAL A SQL")
        print("=" * 60)
        print(f"Carpeta HTML: {self.html_dir}")
        print(f"Carpeta salida: {self.output_dir}")
        print()

        # Paso 1: Obtener slugs desde los índices
        print("Paso 1: Leyendo índices de letras...")
        slugs = self._extraer_slugs_de_indice()
        print(f"  Encontrados {len(slugs)} slugs de jugadores")
        print()

        # Paso 2: Procesar cada jugador
        print("Paso 2: Procesando jugadores...")
        jugadores = []
        selecciones_jugador = []
        errores = 0

        for i, slug in enumerate(slugs, 1):
            html_file = os.path.join(self.html_dir, f'{slug}.html')

            if not os.path.exists(html_file):
                continue

            try:
                with open(html_file, 'r', encoding='utf-8') as f:
                    html = f.read()

                info = self._extraer_info_jugador(html)

                if not info.get('nombre_completo') and not info.get('nombre_display'):
                    continue

                jugador_id = self.jugador_id_counter
                self.jugador_id_counter += 1

                jugadores.append({
                    'id': jugador_id,
                    'slug': slug,
                    'nombre': info.get('nombre_completo') or info.get('nombre_display', slug),
                    'fecha_nacimiento': info.get('fecha_nacimiento'),
                    'lugar_nacimiento': info.get('lugar_nacimiento'),
                    'altura': info.get('altura'),
                    'apodo': info.get('apodo'),
                    'sitio_web': info.get('sitio_web'),
                    'posicion': info.get('posicion'),
                    'selecciones': info.get('selecciones', []),
                    'mundiales': info.get('mundiales_detalle', []),
                })

                # Guardar selecciones
                for sel in info.get('selecciones', []):
                    selecciones_jugador.append({
                        'jugador_id': jugador_id,
                        'jugador_slug': slug,
                        'pais': sel['nombre'],
                        'pais_slug': sel['slug']
                    })

                if i % 500 == 0:
                    print(f"  Procesados {i}/{len(slugs)} jugadores...")

            except Exception as e:
                errores += 1
                print(f"  Error en {slug}: {e}")

        print(f"  Total procesados: {len(jugadores)}")
        print(f"  Total errores: {errores}")
        print()

        # Paso 3: Generar SQL
        print("Paso 3: Generando archivos SQL...")
        self._generar_sql_jugadores(jugadores)
        self._generar_sql_selecciones_jugador(selecciones_jugador, jugadores)

        print()
        print("=" * 60)
        print("COMPLETADO")
        print("=" * 60)

        return {
            'total_jugadores': len(jugadores),
            'total_selecciones': len(selecciones_jugador),
            'errores': errores
        }

    def _generar_sql_jugadores(self, jugadores: List[Dict]):
        """Genera el archivo SQL con INSERTs para la tabla Jugador."""
        output_file = os.path.join(self.output_dir, 'insert_jugadores.sql')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("-- INSERTs para tabla Jugador\n")
            f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"-- Total: {len(jugadores)} jugadores\n\n")

            for jug in jugadores:
                # Preparar valores
                id_ju = jug['id']
                nombre_ju = self._escape_sql(self._truncate(jug['nombre'], 150))

                # Fecha de nacimiento
                fecha_parsed = self._parse_fecha_nacimiento(jug.get('fecha_nacimiento'))
                fecha_ju = fecha_parsed if fecha_parsed else 'NULL'

                lugar_raw = jug.get('lugar_nacimiento') or ''
                lugar_ju = f"'{self._escape_sql(self._truncate(lugar_raw, 200))}'" if lugar_raw.strip() else 'NULL'

                # Altura - solo primeros 5 caracteres (ej: "1.70")
                altura_raw = jug.get('altura', '') or ''
                altura_match = re.match(r'(\d+\.\d{2})', altura_raw)
                altura_ju = altura_match.group(1) if altura_match else ''
                altura_ju = f"'{altura_ju}'" if altura_ju else 'NULL'

                apodo_raw = jug.get('apodo') or ''
                apodo_ju = f"'{self._escape_sql(self._truncate(apodo_raw, 75))}'" if apodo_raw.strip() else 'NULL'

                sitio_web = jug.get('sitio_web') or ''
                if sitio_web.strip():
                    # Extraer solo el dominio si es muy largo
                    if len(sitio_web) > 50:
                        match = re.match(r'https?://([^/]+)', sitio_web)
                        sitio_web = match.group(1) if match else sitio_web[:50]
                    pagina_web_ju = f"'{self._escape_sql(sitio_web)}'"
                else:
                    pagina_web_ju = 'NULL'

                f.write(f"INSERT INTO Jugador (id_ju, nombre_ju, fecha_nacimiento_ju, lugar_cacimiento_ju, altura_ju, apodo_ju, pagina_web_ju) VALUES ({id_ju}, '{nombre_ju}', {fecha_ju}, {lugar_ju}, {altura_ju}, {apodo_ju}, {pagina_web_ju});\n")

        print(f"  Generado: {output_file}")

    def _generar_sql_selecciones_jugador(self, selecciones: List[Dict], jugadores: List[Dict]):
        """Genera archivo auxiliar con las selecciones de cada jugador."""
        output_file = os.path.join(self.output_dir, 'jugador_selecciones.sql')

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("-- Selecciones de cada jugador (para referencia)\n")
            f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- Esto NO es para INSERT directo, es para ayudar a generar Posicion_Jugador\n\n")

            for sel in selecciones:
                f.write(f"-- Jugador ID {sel['jugador_id']} ({sel['jugador_slug']}) -> {sel['pais']} ({sel['pais_slug']})\n")

        print(f"  Generado: {output_file}")

        # Generar archivo con detalle de mundiales para Posicion_Jugador
        output_file2 = os.path.join(self.output_dir, 'jugador_mundiales_detalle.sql')

        with open(output_file2, 'w', encoding='utf-8') as f:
            f.write("-- Detalle de mundiales por jugador (para generar Posicion_Jugador)\n")
            f.write(f"-- Generado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("-- Columnas: jugador_id, mundial, pais, posicion, numero_camiseta, capitan, titular\n\n")

            for jug in jugadores:
                for md in jug.get('mundiales', []):
                    posicion_abrev = self._abreviar_posicion(md.get('posicion', ''))
                    f.write(f"-- {jug['id']}, {md['mundial']}, {md.get('pais', '')}, {posicion_abrev}, {md.get('numero_camiseta', '')}, {md.get('capitan', 0)}, {md.get('titular', 0)}\n")

        print(f"  Generado: {output_file2}")

    def _abreviar_posicion(self, posicion: str) -> str:
        """Convierte posición completa a abreviatura de 2 caracteres."""
        posicion = posicion.lower().strip()

        if 'portero' in posicion or 'arquero' in posicion or 'goalkeeper' in posicion:
            return 'GK'
        elif 'defensa' in posicion or 'defensor' in posicion or 'defender' in posicion:
            return 'DF'
        elif 'centrocampista' in posicion or 'mediocampista' in posicion or 'medio' in posicion or 'midfielder' in posicion:
            return 'MF'
        elif 'delantero' in posicion or 'atacante' in posicion or 'forward' in posicion:
            return 'FW'
        else:
            return posicion[:2].upper() if posicion else ''


if __name__ == '__main__':
    processor = JugadoresLocalProcessor()
    result = processor.process_all()
    print(f"\nResumen: {result}")
