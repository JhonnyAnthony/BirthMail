from flask import jsonify, make_response
from api.services.services import GetCargos

def get_cargos():
    try:
        teste = GetCargos()
        cargos = teste.cargos()
        response = jsonify(cargos)
        response.status_code = 200
    except Exception as e:
        response = make_response(jsonify({"error": str(e)}), 500)
    return response