from flask import Blueprint, jsonify
from controllers.paises_controller import PaisesController

paises_bp = Blueprint('paises', __name__)

controller = PaisesController()

#Routes/paises_route.py
@paises_bp.route('/paises-completos')
def todos_paises_completos():
    controller = PaisesController()
    paises = controller.scrape_info_paises()  # 🚀 SIN LÍMITE
    csv_result = controller.generar_csv_completo(paises)
    
    return jsonify({
        'success': True,
        'total': len(paises),
        'data': paises,
        **csv_result
    })