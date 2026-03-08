from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.mundiales_route import mundiales_bp
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

# Blueprint /api/mundiales
app.register_blueprint(mundiales_bp, url_prefix='/api/mundiales')

@app.route('/')
def home():
    return {
        "mensaje": "🧉 MUNDIALES SCRAPER - USAC DB2 FASE 1",
        "endpoints": [
            "/api/mundiales/scrape - Extrae datos",
            "/api/mundiales/csv - Genera CSVs"
        ]
    }

if __name__ == '__main__':
    app.run(debug=True, port=5000)
