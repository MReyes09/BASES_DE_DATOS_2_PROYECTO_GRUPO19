from flask import Blueprint, jsonify
from controllers.mundiales_controller import MundialesController

mundiales_bp = Blueprint('mundiales', __name__)

controller = MundialesController()

# routes/mundiales_route.py
@mundiales_bp.route('/mundiales-completos')
def todos_mundiales_completos():
    controller = MundialesController()
    mundiales = controller.scrape_info_mundial()  # 🚀 SIN LÍMITE
    csv_result = controller.generar_csv_completo(mundiales)
    
    return jsonify({
        'success': True,
        'total': len(mundiales),
        'data': mundiales,  # Solo muestra 5 en respuesta
        **csv_result
    })
