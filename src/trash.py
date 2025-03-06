from connectionDB import Database
from datetime import datetime, timedelta
import locale
import logging

class TempoCasa:
    def __init__(self):
        self.db_connection = Database()
        self.db_connection.connectData()
        self.data = {}
        self.supervisores = {}
        locale.setlocale(locale.LC_TIME, 'pt_BR')

    def connectionDB(self):
        db_results = self.db_connection.query_tempoCasa()
        for data in db_results:
            self._process_user(data)

    def _process_user(self, data):
        def format_date(date):
            return self._parse_date(date).strftime("%d/%m/%Y")

        data_adm = format_date(data.DATADM)
        aniversario_empresa = self._parse_date(data.DATADM).strftime("%d/%m")
        data_dem = format_date(data.DATAFA) if data.DATAFA != datetime(1900, 12, 31) else datetime.now().strftime("%d/%m/%Y")
        cpf = data.NUMCPF
        situacao = data.SITAFA
        estpos = data.ESTPOS
        postra = data.POSTRA
        email_supervisor = self.db_connection.query_mailsup(estpos, postra)
        nome_supervisor = self.db_connection.query_nomesup(estpos, postra)
        nome = data.NOMFUN

        if cpf not in self.data:
            self.data[cpf] = {
                'nome': nome,
                'situacao': situacao,
                'matriculas': [],
                'data_admissao': data_adm,
                'data_demissao': data_dem,
                'aniversario_empresa': aniversario_empresa,
                'email_pessoal': data.EMAPAR,
                'email_corporativo': data.EMACOM,
                'admissoes': []
            }

        if nome_supervisor:
            if nome_supervisor not in self.supervisores:
                self.supervisores[nome_supervisor] = {
                    "funcionarios": [],
                    "email": email_supervisor
                }
            self.supervisores[nome_supervisor]["funcionarios"].append((nome, aniversario_empresa, situacao))
        
        self.data[cpf]['matriculas'].append((data_adm, data_dem))
        self.data[cpf]['admissoes'].append((data_adm, data_dem))

        if situacao == 1:
            self._check_anniversary(cpf)

    def _parse_date(self, date_str):
        return date_str if isinstance(date_str, datetime) else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def _check_anniversary(self, cpf):
        data_atual = datetime.now()
        primeiro_dia_proximo_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
        ultimo_dia_mes_atual = primeiro_dia_proximo_mes - timedelta(days=1)
        ultimodia = int(ultimo_dia_mes_atual.strftime('%d'))
        matricula = self.data[cpf]['matriculas']
        admissoes = self.data[cpf]['admissoes']
        # tempo_de_casa = self.calcular_tempo_de_casa(admissoes)  
        # lista = self.caso_duas_matriculas(admissoes)
        # anos = tempo_de_casa.days // 365
        # meses = (tempo_de_casa.days % 365) // ultimodia  
        # admissoes.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))

    def filtrar_aniversariantes_do_mes(self):
        aniversariantes = {}
        for supervisor, info in self.supervisores.items():
            for funcionario, aniversario_empresa, situacao in info["funcionarios"]:
                if situacao == 1:
                    if supervisor not in aniversariantes:
                        aniversariantes[supervisor] = {"funcionarios": [], "email": info["email"]}
                    aniversariantes[supervisor]["funcionarios"].append((funcionario, aniversario_empresa, situacao))
        print(aniversariantes)
        return aniversariantes
    def birthMonth(self):
        aniversariantes = self.filtrar_aniversariantes_do_mes()
# Instanciando a classe e chamando o método connectionDB
tet = TempoCasa()
tet.connectionDB()
tet.birthMonth()

def caso_duas_matriculas(self, admissoes):
        lista_duas_matriculas = {}
        admissoes.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
        for supervisor, info in self.supervisores.items(): 
            for funcionario in info["funcionarios"]:
        # Verifica se há mais de uma admissão
                if len(admissoes) > 1:
                    data_demissao_antiga = datetime.strptime(admissoes[-2][1], "%d/%m/%Y")
                    data_admissao_nova = datetime.strptime(admissoes[-1][0], "%d/%m/%Y")
                    diferenca_tempo = data_admissao_nova - data_demissao_antiga
                    if diferenca_tempo < timedelta(days=180):
                        data_admissao_antiga = datetime.strptime(admissoes[-2][0], "%d/%m/%Y")
                        # if data_admissao_antiga > datetime.now():
                        #     return timedelta(0)
                        return datetime.now() - data_admissao_antiga
            if supervisor not in lista_duas_matriculas:
                lista_duas_matriculas[supervisor] = {"funcionarios": [], "email": info["email"]}
        # print(lista_duas_matriculas)
        return lista_duas_matriculas
