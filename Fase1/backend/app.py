from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.mundiales_route import mundiales_bp
from routes.paises_route import paises_bp
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

# Blueprint /api/mundiales
app.register_blueprint(mundiales_bp, url_prefix='/api/mundiales')
# Blueprint /api/paises
app.register_blueprint(paises_bp, url_prefix='/api/paises')

@app.route('/')
def home():
    return {
        "mensaje": "🧉 MUNDIALES SCRAPER - USAC DB2 FASE 1",
        "endpoints": [
            "/api/mundiales/scrape - Extrae datos",
            "/api/paises/scrape - Extrae datos"
        ]
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)
