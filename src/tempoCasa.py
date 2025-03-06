from connectionDB import Database
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import locale
from config import client_secret, client_id, tenant_id, scope, email_from
import requests
import logging
import json

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
        self.hoje = datetime.now().strftime("%d/%m")
        data_adm = format_date(data.DATADM)
        aniversario_empresa = self._parse_date(data.DATADM).strftime("%d/%m")
        mes_aniversario_empresa = self._parse_date(data.DATADM).strftime("%m")
        data_dem = format_date(data.DATAFA) if data.DATAFA != datetime(1900, 12, 31) else datetime.now().strftime("%d/%m/%Y")
        cpf = data.NUMCPF
        situacao = data.SITAFA
        estpos = data.ESTPOS
        postra = data.POSTRA
        local = data.NOMLOCAL
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
            self.supervisores[nome_supervisor]["funcionarios"].append({
                "nome": nome,
                "aniversario_empresa": aniversario_empresa,
                "data_admissao": data_adm,
                "mes_aniversario_empresa": mes_aniversario_empresa,
                "situacao": situacao,
                "setor": local  # Assuming 'local' is the sector
            })
        
        self.data[cpf]['matriculas'].append((data_adm, data_dem))
        self.data[cpf]['admissoes'].append((data_adm, data_dem))

        if data.SITAFA == 1:
            self._check_anniversary(cpf, nome)

    def _parse_date(self, date_str):
        return date_str if isinstance(date_str, datetime) else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def filtrar_aniversariantes_do_mes(self):
        aniversariantes = {}
        mes_atual = datetime.now().strftime("%m")
        for supervisor, info in self.supervisores.items():
            for funcionario in info["funcionarios"]:
                if funcionario["situacao"] != 7 and mes_atual == funcionario["mes_aniversario_empresa"]:
                    if supervisor not in aniversariantes:
                        aniversariantes[supervisor] = {"funcionarios": [], "email": info["email"]}
                    aniversariantes[supervisor]["funcionarios"].append(funcionario)
        return aniversariantes

    # def filtrar_datas(self, aniversariantes):
    #     datas = []
    #     for supervisor, info in aniversariantes.items():
    #         for funcionario in info["funcionarios"]:
    #             datas.append(funcionario["aniversario_empresa"])  # Adiciona a data de aniversário
    #     return datas

    def birthJob(self):
        aniversariantes = self.filtrar_aniversariantes_do_mes()
        # data_aniversario_empresa = self.filtrar_datas(aniversariantes)
        if aniversariantes:
            self._send_supervisor_mail(aniversariantes)
        
    
    def _converter_data(self, data_str):
        return datetime.strptime(f"{data_str}/2024", "%d/%m/%Y")

    def _check_anniversary(self, cpf,nome):
        data_atual = datetime.now()
        primeiro_dia_proximo_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
        ultimo_dia_mes_atual = primeiro_dia_proximo_mes - timedelta(days=1)
        ultimodia = int(ultimo_dia_mes_atual.strftime('%d'))
        matricula = self.data[cpf]['matriculas']
        admissoes = self.data[cpf]['admissoes']
        tempo_de_casa = self.calcular_tempo_de_casa(admissoes)  
        lista = self.caso_duas_matriculas(admissoes)
        anos = tempo_de_casa.days // 365
        meses = (tempo_de_casa.days % 365) // ultimodia  
        admissoes.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
        hoje = datetime.now().strftime("%d/%m")
        if anos > 1:
            # print(f"Aniversário de empresa de {nome.upper()} de {anos} {'anos' if anos > 1 else 'ano'} e {meses} {'meses' if meses > 1 else 'mês'} ")
            self._apply_filters(anos, self.data[cpf])
    def _apply_filters(self, anos, info):
        funcoes = {key: self._send_mail_star for key in (5, 10, 15, 20, 25, 30)}
        funcao = funcoes.get(anos, self.filtrar_aniversariantes)
        funcao(info, anos)
    def calcular_tempo_de_casa(self, admissoes):
        data_admissao = datetime.strptime(admissoes[-1][0], "%d/%m/%Y")
        if data_admissao > datetime.now():
            return timedelta(0)
        return datetime.now() - data_admissao
    
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
    def filtrar_aniversariantes(self, info, anos):
        # print(f"Filtrando aniversariantes para {anos} anos")  
        self._send_mail_year(info, anos)
    def _send_supervisor_mail(self, aniversariantes):
        count = 0
        hoje = datetime.now().strftime("%d/%m")
        mesStart = datetime.now().month
        diaFixo = 6 
        data_fixa = datetime(datetime.now().year, mesStart, diaFixo)
        diaStart = data_fixa.strftime("%d/%m")
        if hoje == diaStart:
            for supervisor, info in aniversariantes.items(): 
                count += 1
                # emailSupervisor = info["email"]       #---------------------PRD-----------------------------
                emailSupervisor = ["jhonny.souza@fgmdentalgroup.com"]    #---------------------QAS-----------------------------
                funcionarios = info["funcionarios"]     
                mes_seguinte = datetime.now() + relativedelta(months=1)
                mes_seguinte = mes_seguinte.strftime("%B").title()
                subject = f'Aniversariantes do mês de {mes_seguinte}' # Define o assunto do e-mail 
                body = self._generate_supervisor_email_body(funcionarios, mes_seguinte, supervisor) # Gera o corpo do e-mail 
                logging.info(f'Lista de Aniversáriantes de {supervisor} do mes de {mes_seguinte}')
                # print(f"Contagem: {count}")
                # self._send_email(emailSupervisor, subject, body) # Envia o e-mail
    def _send_mail_year(self, info, anos):
        if self.hoje in info['aniversario_empresa']:
            print(info['nome'].title())
            email = ["jhonny.souza@fgmdentalgroup.com"]  # ---------------------QAS-----------------------------
            # email = [f"{info['email_pessoal']}",f"{info['email_corporativo']}"]  # ---------------------PRD-----------------------------
            subject = f"Parabéns pelos {anos} anos de Casa {info['nome'].title()}!"
            body = self._generate_year_body( f'https://fgmdentalgroup.com/wp-content/uploads/2025/02/{anos}-anos.jpg','ImageBirth', None) #-----
            logging.info(f"Aniversáriantes da Empresa de {info['nome'].title()} Enviada para {email}")
            self._send_email(email, subject, body)

    def _send_mail_star(self, info, anos):
        if self.hoje in info['aniversario_empresa']:
            email = ["jhonny.souza@fgmdentalgroup.com"]  # ---------------------QAS-----------------------------
            # email = [f"{info['email_pessoal']}",f"{info['email_corporativo']}"]  # ---------------------PRD-----------------------------
            subject = f"Parabéns pelos {anos} anos de Casa {info['nome'].title()}!"
            body = self._generate_year_body(f'https://fgmdentalgroup.com/wp-content/uploads/2025/02/{anos}-anos-estrela.jpg', 'ImageBirth', f'https://fgmdentalgroup.com/Endomarketing/Tempo%20de%20casa/{anos}%20anos/index.html')
            print(f"Aniversáriantes da Empresa de {info['nome'].title()} Enviada para {email}, {info['nome']}")
            self._send_email(email, subject, body)
    def _generate_supervisor_email_body(self, funcionarios, mes_seguinte, supervisor):
        body = f"<strong>Olá {supervisor.title()}. Segue a lista de colaboradores que fazem aniversário de empresa no mês de {mes_seguinte}:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += """<tr style="background-color: #d3d3d3; color: black;"><th>Colaboradores Aniversáriantes</th><th>Data</th><th>Setor</th><th>Tempo de Empresa</th></tr>""" 

        # Ordene os funcionários por data de aniversário
        funcionarios_ordenados = sorted(funcionarios, key=lambda x: self._converter_data(x["aniversario_empresa"]))
        for funcionario in funcionarios_ordenados:
            tempo_de_empresa = self.calcular_tempo_de_casa([(funcionario['data_admissao'], datetime.now().strftime("%d/%m/%Y"))])
            anos = tempo_de_empresa.days // 365
            if funcionario['aniversario_empresa'] <= datetime.now().strftime("%d/%m"):
                anos = anos
            else:
                anos = anos + 1
            body += f"<tr><td>{funcionario['nome']}</td><td>{funcionario['aniversario_empresa']}</td><td>{funcionario['setor']}</td><td>{anos} {'anos' if anos > 1 else 'ano'}</td></tr>"
        body += "</table><br>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_year_body(self,image_src, alt_text, link=None):
        if link:
            return f"""<html><br><body style="display: flex; justify-content: center; align-items: center;height: auto; margin: 0;">
                        <a href="{link}" style="display: flex; justify-content: center; align-items: center;">
                            <img src="{image_src}" alt="{alt_text}">
                        </a></body></html>"""
        else:
            return f"""<html><br><body style="display: flex; justify-content: center; align-items: center;height: auto; margin: 0;">
                        <a style="display: flex; justify-content: center; align-items: center;">
                            <img src="{image_src}" alt="{alt_text}">
                        </a></body></html>"""    
    
        

    def _send_email(self, email_to, subject, body):
        email_group = email_to
        token = self._get_access_token()
        to_recipients = [{'emailAddress': {'address': email}} for email in email_group]
        
        url = f'https://graph.microsoft.com/v1.0/users/{email_from}/sendMail'
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        email_msg = {
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'HTML',
                    'content': body
                },
                'toRecipients': to_recipients
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(email_msg))
        
        if response.status_code == 202:
            logging.info(f"E-mail enviado para {email_group}")
            logging.info("------------------------------------------------------------------------------------")
            
            
        else:
            logging.error(f'Falha ao enviar e-mail: {response.status_code}: {response.text}')

    def _get_access_token(self):
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope
        }
        response = requests.post(url, data=data)
        return response.json().get('access_token')
if __name__ == '__main__': 
    start = TempoCasa()
    start.connectionDB()
    start.birthJob()