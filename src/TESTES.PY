from connectionDB import Database
from datetime import datetime, timedelta
import locale

class TempoCasa:
    def __init__(self):
        self.db_connection = Database()  # Inicializa a conexão com o banco de dados
        self.db_connection.connectData()  # Conecta ao banco de dados
        self.data = {}  # Inicializa o dicionário para armazenar dados dos funcionários
        locale.setlocale(locale.LC_TIME, 'pt_BR')  # Define a localidade para português do Brasil

    def connectionDB(self):
        db_results = self.db_connection.query_tempoCasa()
        for data in db_results:
            self._process_user(data)  # Processa cada registro de funcionário

    def _process_user(self, data):
        data_adm = self._parse_date(data.DATADM)
        data_dem = self._parse_date(data.DATAFA)  # Supondo que esta seja a data de demissão correta
        email_pessoal = data.EMAPAR
        email_corporativo = data.EMACOM
        matricula = data.NUMCAD
        nome = data.NOMFUN
        situacao = data.SITAFA
        if nome  not in self.data:
            self.data[nome] = {
                'nome': nome,
                'situacao': situacao,
                'matricula': matricula,
                'email_pessoal': email_pessoal,
                'email_corporativo': email_corporativo,

                'admissoes': []
            }
        
        self.data[nome]['admissoes'].append((data_adm, data_dem if data_dem != datetime(1900, 12, 31, 0, 0) else datetime.now()))
        print(self.data)
    def calcular_tempo_de_casa(self, admissoes):
        tempo_total = timedelta(0)
        admissoes.sort()  # Ordena as datas de admissão
        for i in range(len(admissoes)):
            inicio, fim = admissoes[i]
            if i < len(admissoes) - 1:
                proximo_inicio, _ = admissoes[i + 1]
                if (proximo_inicio - fim).days <= 180:  # 180 dias = 6 meses
                    tempo_total += fim - inicio
                else:
                    tempo_total += fim - inicio  # Adiciona o período atual
            else:
                tempo_total += fim - inicio  # Adiciona o último período
        return tempo_total

    def calcular_tempo_total(self):
        for nome, info in self.data.items():
            admissoes = info['admissoes']
            tempo_de_casa = self.calcular_tempo_de_casa(admissoes)
            anos, meses = self._converter_dias_para_anos_meses(tempo_de_casa.days)
            print(f"Funcionário: {info['nome']} - Tempo de casa: {anos} anos e {meses} meses, Matricula: {info['matricula']}")

    def _converter_dias_para_anos_meses(self, dias):
        anos = dias // 365
        meses = (dias % 365) // 30
        return anos, meses

    def _parse_date(self, date_str):
        if isinstance(date_str, datetime):
            return date_str
        return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

start = TempoCasa()
start.connectionDB()
start.calcular_tempo_total()