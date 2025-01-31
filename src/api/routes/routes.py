from flask import jsonify
from api.services.services import GetCargos

def get_cargos():
    cargos = GetCargos.cargos()
    response = jsonify(cargos)
    return response
