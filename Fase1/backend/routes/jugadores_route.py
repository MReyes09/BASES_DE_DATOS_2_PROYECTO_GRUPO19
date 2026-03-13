from flask import Blueprint, jsonify, request
from controllers.jugadores_controller import JugadoresController

jugadores_bp = Blueprint('jugadores', __name__)


def _json_error(exc: Exception, code: int = 502):
    return jsonify({'success': False, 'error': str(exc)}), code


@jugadores_bp.route('/scrape-all')
def scrape_all_players():
    try:
        controller = JugadoresController()
        result = controller.scrape_all_players()
        return jsonify(result)
    except Exception as exc:
        return _json_error(exc)


@jugadores_bp.route('/scrape-country/<country_slug>')
def scrape_country(country_slug):
    try:
        controller = JugadoresController()
        result = controller.scrape_single_country(country_slug)
        return jsonify(result)
    except ValueError as exc:
        return _json_error(exc, 400)
    except Exception as exc:
        return _json_error(exc)


@jugadores_bp.route('/scrape-player/<player_slug>')
def scrape_player(player_slug):
    try:
        country = request.args.get('country', 'Desconocido')
        controller = JugadoresController()
        detail = controller.scrape_single_player(player_slug, country)
        return jsonify(detail)
    except Exception as exc:
        return _json_error(exc)


@jugadores_bp.route('/countries')
def list_countries():
    try:
        controller = JugadoresController()
        paises = controller.get_countries()
        return jsonify({'total': len(paises), 'paises': paises})
    except Exception as exc:
        return _json_error(exc)


@jugadores_bp.route('/country-players/<country_slug>')
def list_country_players(country_slug):
    try:
        controller = JugadoresController()
        jugadores = controller.get_country_players(country_slug)
        return jsonify({'total': len(jugadores), 'jugadores': jugadores})
    except ValueError as exc:
        return _json_error(exc, 400)
    except Exception as exc:
        return _json_error(exc)


@jugadores_bp.route('/scrape-local')
def scrape_local():
    """Procesa todos los HTML locales de jugadores sin hacer requests."""
    try:
        controller = JugadoresController()
        result = controller.scrape_local_html_dir()
        return jsonify(result)
    except Exception as exc:
        return _json_error(exc)
