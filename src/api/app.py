from fastapi import FastAPI
from datetime import datetime
from typing import List, Dict
from schemas import Category, CoordenadorItem, Item, SubordinadoItem,Connection


app = FastAPI()



connection_instance = Connection()
results = connection_instance.connection()

subordinados: Dict[str, SubordinadoItem] = {}
coordenadores: Dict[str, CoordenadorItem] = {}
subordinate_id_counter = 1
coordenador_id_counter = 1

for result in results:
    nome_sup = result.NOMESUP
    nome_completo = result.NOMFUN
    cargo = result.TITCAR.title()
    idPos = result.IDEPOS
    dataNas = result.DATNAS
    if not isinstance(dataNas, datetime):
        dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
    data_nascimento = dataNas.strftime("%d/%m")
    
    if nome_completo not in subordinados:
        subordinados = SubordinadoItem(id=subordinate_id_counter, nome=nome_completo.title(), data_nas=data_nascimento, cargo=cargo, idPos=idPos, category=Category.EMPLOYEE)
        subordinate_id_counter += 1
    if nome_sup:
        if nome_sup not in coordenadores:
            coordenadores[nome_sup] = CoordenadorItem(id=coordenador_id_counter, nome=nome_sup.title(), cargo=cargo, data_nas=data_nascimento, idPos=idPos, category=Category.COORDENADOR)
            coordenador_id_counter += 1


    if nome_sup:
        coordenadores[nome_sup].subordinados.append(subordinados)

@app.get("/")
def index() -> List[CoordenadorItem]:
    return list(coordenadores.values())

