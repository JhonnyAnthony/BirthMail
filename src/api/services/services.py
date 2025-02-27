from connectionDB import Database
from datetime import datetime

class Connection:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def connection(self):
        return self.db.query_principal()
class GetCargos:
    def __init__(self):
        pass
    def cargos():
        connection_instance = Connection()
        results = connection_instance.connection()
        # Dicionário para armazenar todos os cargos com base no ID
        cargos_dict = {}
        id = 0
        for result in results:
            id += 1
            setor = result.NOMLOCAL
            nome_sup = result.NOMESUP   #if result.NOMESUP else 'BIANCA DE OLIVEIRA LUIZ MITTELSTADT'# Tratar null
            nome_completo = result.NOMFUN
            cargo = result.TITCAR.title()
            idPos = result.IDEPOS
            dataNas = result.DATNAS
            datAdm = result.DATADM
            if not isinstance(dataNas, datetime):
                datAdm = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
                dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
            data_admissao = datAdm.strftime("%d/%m/%y")
            data_aniversario = dataNas.strftime("%d/%m")

            cargos_dict[id] = {
                "id": id,
                "idPos": idPos,
                "setor": setor,
                "data_admissao":data_admissao,
                "data_aniversario": data_aniversario,
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
        return hierarchy