import sys
sys.path.append('C:/Github/BirthMail/src')
from flask import Flask
from api.routes.routes import get_cargos

app = Flask(__name__)

@app.route('/cargos', methods=['GET'])
def cargos_route():
    return get_cargos()
# set FLASK_APP=app.py & flask run
if __name__ == '__main__':
    app.run(debug=True)
