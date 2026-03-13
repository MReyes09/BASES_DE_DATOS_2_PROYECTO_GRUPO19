from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from routes.jugadores_route import jugadores_bp
from controllers.jugadores_controller import JugadoresController
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config['DEBUG'] = True

# Blueprint /api/jugadores
app.register_blueprint(jugadores_bp, url_prefix='/api/jugadores')


@app.route('/')
def home():
    controller = JugadoresController()
    return {
        'mensaje': 'SCRAPER DE JUGADORES - MAIN INDEPENDIENTE',
        'output_dir': controller.data_dir,
        'endpoints': [
            '/api/jugadores/scrape-all - Scrape todos los jugadores',
            '/api/jugadores/scrape-country/<slug> - Scrape una seleccion',
            '/api/jugadores/scrape-player/<slug> - Scrape un jugador',
            '/api/jugadores/countries - Lista de paises',
            '/api/jugadores/country-players/<slug> - Jugadores de un pais',
        ],
    }


if __name__ == '__main__':
    port = int(os.getenv('JUGADORES_PORT', '5001'))
    app.run(debug=True, port=port)
