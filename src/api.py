import logging
from fastapi import FastAPI
from connectionDB import Database
from datetime import datetime
from typing import List, Dict
from models import DiretorItem,SupervisorItem,Category,CoordenadorItem,Item
app = FastAPI()
# uvicorn src/api:app --reload  
class Connection:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def connection(self):
        return self.db.query()
connection_instance = Connection()
results = connection_instance.connection()

diretores: Dict[str, DiretorItem] = {}
supervisores: Dict[str, SupervisorItem] = {}
coordenadores: Dict[str, CoordenadorItem] = {}
subordinate_id_counter = 1
coordenador_id_counter = 1
supervisor_id_counter = 1
diretor_id_counter = 1

for result in results:
    nome_sup = result.NOMESUP
    nome_completo = result.NOMFUN
    dataNas = result.DATNAS
    if not isinstance(dataNas, datetime):
        dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
    data_nascimento = dataNas.strftime("%d/%m")
    cargo = result.TITCAR
    supervisor_name = nome_sup # Assuming there is a supervisor name field
    diretor_name = result.NOMESUP # Assuming there is a director name field

    if diretor_name and diretor_name not in diretores:
        diretores[diretor_name] = DiretorItem(id=diretor_id_counter, nome=diretor_name, cargo=cargo, data_nas=data_nascimento, category=Category.DIRETOR)
        diretor_id_counter += 1
        
    if supervisor_name and supervisor_name not in supervisores:
        supervisores[supervisor_name] = SupervisorItem(id=supervisor_id_counter, nome=supervisor_name, cargo=cargo, data_nas=data_nascimento, category=Category.SUPERIOR)
        supervisor_id_counter += 1
    
    if nome_sup:
        if nome_sup not in coordenadores:
            coordenadores[nome_sup] = CoordenadorItem(id=coordenador_id_counter, nome=nome_sup, cargo=cargo, data_nas=data_nascimento, category=Category.SUPERIOR)
            coordenador_id_counter += 1

        if nome_completo:
            subordinado = Item(id=subordinate_id_counter, nome=nome_completo, data_nas=data_nascimento, cargo=cargo, category=Category.EMPLOYEE)
            coordenadores[nome_sup].subordinados.append(subordinado)
            subordinate_id_counter += 1

        if supervisor_name and nome_sup not in [coordenador.nome for coordenador in supervisores[supervisor_name].coordenadores]:
            supervisores[supervisor_name].coordenadores.append(coordenadores[nome_sup])

        if diretor_name and supervisor_name not in [supervisor.nome for supervisor in diretores[diretor_name].supervisores]:
            diretores[diretor_name].supervisores.append(supervisores[supervisor_name])

@app.get("/")
def index() -> List[DiretorItem]:
    return list(diretores.values())
