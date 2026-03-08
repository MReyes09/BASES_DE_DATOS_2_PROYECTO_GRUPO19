import requests
from bs4 import BeautifulSoup
import csv
import os
import time
import re
from dotenv import load_dotenv
from typing import List, Dict, Any

load_dotenv()

class PaisesController:
    def __init__(self):
        self.base_url = os.getenv('BASE_URL', 'https://www.losmundialesdefutbol.com')
        self.headers = {
            'User-Agent': os.getenv('USER_AGENT', 
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)
    
    def scrape_info_paises(self) -> List[Dict[str, Any]]:
        """🎯 TODO: Lista paises"""
        paises = self._extraer_paises()
        print(f"✅ {len(paises)} países encontrados")
        
        paises_format = []
        for i, p in enumerate(paises, 1):
            print(f"\n🌍 [{i}/{len(paises)}] Procesando {p}...")
            paises_format.append({
                'nombre_pais': p
            })

        return paises_format
        
    def _extraer_paises(self) -> List[str]:
        """🔍 Extrae lista de paises"""
        url = f"{self.base_url}/jugadores.php"
        response = self.session.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        a_tags = soup.select('div.a-left a[href] img')
        paises = []

        for img in a_tags:
            pais = img.find_parent('a').get_text(strip=True).split()[-1]
            if len(pais) > 2:
                paises.append(pais) 

        print(f"✅ EXTRAÍDOS {len(paises)} países")
        return sorted(list(set(paises)))

    def generar_csv_completo(self, paises: List[Dict[str, Any]]) -> Dict:
        """💾 CSV para Postgres"""
        os.makedirs('data', exist_ok=True)
        filename = 'data/paises_completos.csv'

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['nombre_pais'])
            for pais in paises:
                writer.writerow([pais['nombre_pais']])
        
        return {
            'success': True,
            'archivo': filename,
            'total': len(paises)
        }
