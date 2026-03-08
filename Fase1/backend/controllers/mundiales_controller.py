import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import re
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class MundialesController:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'https://www.losmundialesdefutbol.com')
        self.headers = {
            'User-Agent': os.getenv('USER_AGENT', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_info_mundial(self) -> List[Dict[str, Any]]:
        """🎯 TODO: Lista mundiales + sedes (SIN LÍMITE)"""
        mundiales = self._extraer_anio_mundiales()
        print(f"✅ {len(mundiales)} mundiales encontrados")
        
        mundiales_completos = []
        for i, m in enumerate(mundiales, 1):
            print(f"\n🏆 [{i}/{len(mundiales)}] Procesando {m['año']}...")
            sede = self._extraer_sede_mundial(m['año'])
            mundiales_completos.append({
                'año': m['año'],
                'sede': sede,
                'url_mundial': m['url_mundial']
            })
            time.sleep(1)
        
        print(f"✅ PROCESADOS {len(mundiales_completos)} mundiales completos")
        return mundiales_completos
    
    def _extraer_anio_mundiales(self) -> List[Dict[str, Any]]:
        """🔍 Extrae lista de 23 mundiales"""
        url = f"{self.base_url}/mundiales.php"
        response = self.session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        tabla = soup.find('table', class_='c0s5 color-alt')
        if not tabla:
            return []
        
        mundiales = []
        rows = tabla.find_all('tr', class_='a-center')
        for row in rows:
            td_mundial = row.find('td', class_='a-top')
            if td_mundial:
                a_tag = td_mundial.find('a')
                if a_tag and 'Mundial' in a_tag.get_text():
                    texto = a_tag.get_text(strip=True)
                    año_str = ''.join(filter(str.isdigit, texto))
                    if len(año_str) >= 4:
                        mundiales.append({
                            'año': int(año_str[-4:]),
                            'url_mundial': a_tag.get('href', '')
                        })
        return mundiales
    
    def _extraer_sede_mundial(self, año: int) -> str:
        """🎯 Extrae SOLO sede de un mundial"""
        url = f"{self.base_url}/mundiales/{año}_mundial.php"
        try:
            response = self.session.get(url, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            for elem in soup.find_all(['p', 'div', 'span']):
                texto = elem.get_text(strip=True)
                if "Organizador" in texto:
                    if "- Organizador:" in texto:
                        sede = texto.split("- Organizador:")[1].split("-")[0].strip()
                    else:
                        sede = texto.split("Organizador:")[1].split("-")[0].strip()
                    return sede
            return "N/A"
        except:
            return "ERROR"
    
    def generar_csv_completo(self, mundiales: List[Dict]) -> Dict:
        """💾 CSV para Postgres"""
        os.makedirs('data', exist_ok=True)
        filename = 'data/mundiales_completos.csv'
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['año', 'sede'])
            for m in mundiales:
                writer.writerow([m['año'], m['sede']])
        
        return {
            'success': True,
            'archivo': filename,
            'total': len(mundiales)
        }
