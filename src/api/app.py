from flask import Flask, jsonify
from schemas import Connection
from datetime import datetime

app = Flask(__name__)

@app.route('/cargos', methods=['GET'])
def get_cargos():
    connection_instance = Connection()
    results = connection_instance.connection()

    # Dicionário para armazenar todos os cargos com base no ID
    cargos_dict = {}
    id = 0
    for result in results:
        id += 1
        setor = result.NOMLOC
        nome_sup = result.NOMESUP   if result.NOMESUP else 'BIANCA DE OLIVEIRA LUIZ MITTELSTADT'# Tratar null
        nome_completo = result.NOMFUN
        cargo = result.TITCAR.title()
        idPos = result.IDEPOS
        dataNas = result.DATNAS
        if not isinstance(dataNas, datetime):
            dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
        data_nascimento = dataNas.strftime("%d/%m")

        cargos_dict[id] = {
            "id": id,
            "idPos": idPos,
            "setor": setor,
            "data_nascimento": data_nascimento,
            "nome_sup": nome_sup,
            "nome_completo": nome_completo,
            "cargo": cargo,
            "subordinados": []
        }

    # Construir a hierarquia
    hierarchy = []
    for cargo in cargos_dict.values():
        nome_sup = cargo["nome_sup"]
        
        if nome_sup != 'BIANCA DE OLIVEIRA LUIZ MITTELSTADT':
            superior = next((sup for sup in cargos_dict.values() if sup["nome_completo"] == nome_sup), None)
            if superior:
                superior["subordinados"].append(cargo)
            else:
                    hierarchy.append(cargo)
        else:
            hierarchy.append(cargo)

    return jsonify(hierarchy)

if __name__ == '__main__':
    app.run(debug=True)
