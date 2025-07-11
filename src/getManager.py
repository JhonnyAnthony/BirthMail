import requests
from connectionDB import Database
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import client_secret, client_id, tenant_id, scope, email_from
import json
import logging
import locale

class Manager:
    def __init__(self):
        self.db_connection = Database()  # Inicializa a conexão com o banco de dados
        self.db_connection.connectData()  # Conecta ao banco de dados
        self.supervisores = {}  # Dicionário para armazenar supervisores e seus funcionários
        # locale.setlocale(locale.LC_TIME, 'pt_BR')  # Define a localidade para português do Brasil
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Define a localidade para português do Brasil

    def connectionDB(self):
        try:
            db_results = self.db_connection.query_principal()
            for data in db_results:
                self._process_user(data)  # Processa cada registro de funcionário
        except Exception as e:
            logging.error("Error processing database results: %s", e)

    def _process_user(self, data):
        try:
            self.situacao = data.SITAFA
            local = data.NOMLOCAL
            usuario = data.USERSUP if hasattr(data, 'USERSUP') else None
            if usuario == 'bianca':
                usuario = "aline.mira"
            data_nascimento = self._parse_date(data.DATNAS)
            nome_funcionario = self._format_name(data.NOMFUN)
            self.hoje = datetime.now().strftime("%d/%m")
            mes_nascimento = data_nascimento.strftime("%m")
            dia_mes_nascimento = data_nascimento.strftime("%d/%m")
            self.email_teste = ["sophia.alberton@fgmdentalgroup.com"]  
            # self.email_teste = ["jhonny.souza@fgmdentalgroup.com"]  
            # Chamando as funções para obter os dados dos supervisores
            estpos = data.ESTPOS
            postra = data.POSTRA
            email_supervisor = [self.db_connection.query_mailsup(estpos, postra)]
            nome_supervisor = self.db_connection.query_nomesup(estpos, postra)
            self.email_rh_list = ["gestaodepessoas@fgmdentalgroup.com", "aline.mira@fgmdentalgroup.com"]  # Email lista mensal
            self.emailToday = ["gestaodepessoas@fgmdentalgroup.com", "grupo.coordenadores@fgmdentalgroup.com", "grupo.supervisores@fgmdentalgroup.com", "grupo.gerentes@fgmdentalgroup.com"]  # Email aniversário diário

            if nome_supervisor:
                if nome_supervisor not in self.supervisores:
                    self.supervisores[nome_supervisor] = {"funcionarios": [], "email": email_supervisor}
                self.supervisores[nome_supervisor]["funcionarios"].append((nome_funcionario, mes_nascimento, dia_mes_nascimento, local))
        except Exception as e:
            logging.error("Error processing user data: %s", e)
    def _format_name(self, name):
        return ' '.join([word.capitalize() for word in name.split()]) if name else ""

    def _parse_date(self, date_str):
        if not isinstance(date_str, datetime):
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_str

    def filtrar_aniversariantes_do_mes(self):
        aniversariantes = {}
        mes_atual = datetime.now().strftime("%m")
        for supervisor, info in self.supervisores.items():
            for funcionario, mes_nascimento, dia_mes_nascimento, local in info["funcionarios"]:
                if mes_nascimento == mes_atual:
                    if supervisor not in aniversariantes:
                        aniversariantes[supervisor] = {"funcionarios": [], "email": info["email"]}
                    aniversariantes[supervisor]["funcionarios"].append((funcionario, dia_mes_nascimento, local))
        return aniversariantes

    def filtrar_aniversariantes_do_mes_seguinte(self):
        aniversariantes_mes = {}
        mes_seguinte = datetime.now() + relativedelta(months=1)
        mes_seguinte = mes_seguinte.strftime("%m")
        for supervisor, info in self.supervisores.items():
            for funcionario, mes_nascimento, dia_mes_nascimento, local in info["funcionarios"]:
                if mes_nascimento == mes_seguinte:
                    if supervisor not in aniversariantes_mes:
                        aniversariantes_mes[supervisor] = {"funcionarios": [], "email": info["email"]}
                    aniversariantes_mes[supervisor]["funcionarios"].append((funcionario, dia_mes_nascimento, local))
        return aniversariantes_mes
    def filtrar_datas(self, aniversariantes):
        datas = []
        for supervisor, info in aniversariantes.items():
            for funcionario in info["funcionarios"]:
                datas.append(funcionario[1])  # Adiciona a data de aniversário
        return datas
    
    def birthMonth(self):
        aniversariantes = self.filtrar_aniversariantes_do_mes()
        aniversariantes_mes = self.filtrar_aniversariantes_do_mes_seguinte()
        data_aniversario = self.filtrar_datas(aniversariantes)
        ano = datetime.now().year
        if ano % 4 == 0: ano = 'bissexto' #Verifica se o ano é bissexto
        


        if aniversariantes:
            self._send_birthday_today_mail(aniversariantes, data_aniversario,ano)                  
            self._send_mail_rh(aniversariantes_mes)
            self._send_birth_superior_mail(aniversariantes_mes)
                    
    def _send_birthday_today_mail(self, aniversariantes, data_aniversario,ano):
        if  '29/02' in data_aniversario and ano != 'bissexto' and self.hoje == '27/02':
            # email_morning = self.emailToday       #---------------------PRD-----------------------------
            email_morning = self.email_teste    #---------------------QAS-----------------------------
            subject = f'Aniversariantes do dia'
            body = self._generate_dayling_email_body(aniversariantes,ano)
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info(f'Lista de Aniversáriantes do dia Enviada')
            self._send_email(email_morning, subject, body)
        elif  self.hoje in data_aniversario :
            # email_morning = self.emailToday       #---------------------PRD-----------------------------
            email_morning = self.email_teste    #---------------------QAS-----------------------------
            subject = f'Aniversariantes do dia'
            body = self._generate_dayling_email_body(aniversariantes,ano)
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info(f'Lista de Aniversáriantes do dia Enviada')
            print("Email Aniversário Diário")
            self._send_email(email_morning, subject, body)
        else: 
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info("Sem aniversáriantes no dia!")       

    def _send_mail_rh(self, aniversariantes_mes):
        mesStart = datetime.now().month
        diaFixo = 27
        data_fixa = datetime(datetime.now().year, mesStart, diaFixo)
        diaStart = (data_fixa.strftime("%d/%m"))
        hoje = datetime.now().strftime("%d/%m")
        if hoje == diaStart:
            # email_rh = self.email_rh_list  # ---------------------PRD-----------------------------
            email_rh = self.email_teste  # ---------------------QAS-----------------------------
            mes_seguinte = datetime.now() + relativedelta(months=1)
            mes_seguinte = mes_seguinte.strftime("%B").title()
            subject = f'Aniversariantes do mês de {mes_seguinte}'
            body = self._generate_rh_email_body(aniversariantes_mes,mes_seguinte)
            logging.info(f'Lista de Aniversáriantes do Mes de {mes_seguinte} Enviada para {email_rh}')
            self._send_email(email_rh, subject, body)


    def _send_birth_superior_mail(self, aniversariantes_mes): 
        count = 0
        hoje = datetime.now().strftime("%d/%m")
        mesStart = datetime.now().month
        diaFixo = 27 
        data_fixa = datetime(datetime.now().year, mesStart, diaFixo)
        diaStart = (data_fixa.strftime("%d/%m"))
        if hoje == diaStart:
            for supervisor, info in aniversariantes_mes.items(): 
                count += 1
                # emailSupervisor = info["email"]       #---------------------PRD-----------------------------
                emailSupervisor = self.email_teste    #---------------------QAS-----------------------------
                funcionarios = info["funcionarios"]     
                mes_seguinte = datetime.now() + relativedelta(months=1)
                mes_seguinte = mes_seguinte.strftime("%B").title()
                subject = f'Aniversariantes do mês de {mes_seguinte}' # Define o assunto do e-mail 
                body = self._generate_supervisor_email_body(supervisor, funcionarios,mes_seguinte) # Gera o corpo do e-mail 
                logging.info(f'Lista de Aniversáriantes de {supervisor} do mes de {mes_seguinte}')
                print(f"Contagem: {count}")
                self._send_email(emailSupervisor, subject, body) # Envia o e-mail
    def _converter_data(self, data_str):
        return datetime.strptime(f"{data_str}/2024", "%d/%m/%Y")
    
    def _generate_rh_email_body(self, aniversariantes_mes,mes_seguinte):
        body = f"<strong>Bom dia, Segue a lista de colaboradores que fazem aniversário no mes de {mes_seguinte}:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += """<tr style="background-color: #d3d3d3; color: black;"><th>Colaboradores Aniversáriantes</th><th>Data</th><th>Setor</th></tr>"""
        
        # Colete todos os aniversariantes em uma única lista
        todos_aniversariantes = []
        for supervisor, info in aniversariantes_mes.items():
            for funcionario, dia_mes_nascimento, local in info["funcionarios"]:
                todos_aniversariantes.append((supervisor, funcionario, dia_mes_nascimento, local))
        
        # Ordene todos os aniversariantes por data de aniversário
        todos_aniversariantes.sort(key=lambda x: (int(x[2].split('/')[1]), int(x[2].split('/')[0])))

        # Construa a tabela
        for supervisor, funcionario, dia_mes_nascimento, local in todos_aniversariantes:
            body += f"<tr><td>{funcionario}</td><td>{dia_mes_nascimento}</td><td>{local}</td></tr>"
        
        body += "</table><br>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body


    def _generate_dayling_email_body(self, aniversariantes,ano):
        body = f"<strong>Olá Liderança. Segue a lista de colaboradores que fazem aniversário hoje:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += """<tr style="background-color: #d3d3d3; color: black;"><th>Colaboradores Aniversáriantes</th><th>Data</th><th>Setor</th></tr>""" 

        # Colete todos os aniversariantes em uma única lista
        todos_aniversariantes = []
        for supervisor, info in aniversariantes.items():
            for funcionario, dia_mes_nascimento, local in info["funcionarios"]:
                if self.hoje in dia_mes_nascimento:
                    todos_aniversariantes.append((funcionario, dia_mes_nascimento, local))
                elif dia_mes_nascimento == '29/02' and ano != 'bissexto' and self.hoje == '27/02' : #FILTRO DE ANIVERSÁRIO DIA 29/02 SEM ANO BISSEXTO
                    todos_aniversariantes.append((funcionario, dia_mes_nascimento, local))
        # Ordene todos os aniversariantes por nome do colaborador
        todos_aniversariantes.sort(key=lambda x: x[0])

        # Construa a tabela
        for funcionario, dia_mes_nascimento, local in todos_aniversariantes:
            body += f"<tr><td>🎂{funcionario}</td><td>📅{dia_mes_nascimento}</td><td>{local}</td></tr>"

        body += "</table><br>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body

    def _generate_supervisor_email_body(self, supervisor, funcionarios,mes_seguinte):
        body = f"<strong>Olá {supervisor.title()}. Segue a lista de colaboradores que fazem aniversário no mes de {mes_seguinte}:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += """<tr style="background-color: #d3d3d3; color: black;"><th>Colaboradores Aniversáriantes</th><th>Data</th><th>Setor</th></tr>""" 


        funcionarios_ordenados = sorted(funcionarios, key=lambda x: self._converter_data(x[1]))
        for funcionario, dia_mes_nascimento, local in funcionarios_ordenados:
            body += f"<tr><td>{funcionario}</td><td>{dia_mes_nascimento}</td><td>{local}</td></tr>"
        body += "</table><br>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body

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