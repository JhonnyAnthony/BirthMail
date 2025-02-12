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
        locale.setlocale(locale.LC_TIME, 'pt_BR')  # Define a localidade para português do Brasil

    def connectionDB(self):
        db_results = self.db_connection.query()
        for data in db_results:
            self._process_user(data)  # Processa cada registro de funcionário

    def _process_user(self, data):
        local = data.NOMLOCAL
        usuario = data.USERSUP
        if usuario == 'bianca':
            usuario = "aline.mira"
        data_nascimento = self._parse_date(data.DATNAS)
        nome_funcionario = self._format_name(data.NOMFUN)
        nome_supervisor = self._format_name(data.NOMESUP)
        self.hoje = datetime.now().strftime("%d/%m")
        mes_nascimento = data_nascimento.strftime("%m")
        dia_mes_nascimento = data_nascimento.strftime("%d/%m")
        self.email_teste = ["jhonny.souza@fgmdentalgroup.com"] #-------------------------- QAS ------------------------
        email_supervisor = [f"{usuario}@fgmdentalgroup.com"]  # Email lista colaborador por lider mensal
        self.email_rh_list = ["gestaodepessoas@fgmdentalgroup.com", "aline.mira@fgmdentalgroup.com"] #Email lista mensal
        self.emailToday = ["gestaodepessoas@fgmdentalgroup.com","grupo.coordenadores@fgmdentalgroup.com","grupo.supervisores@fgmdentalgroup.com","grupo.gerentes@fgmdentalgroup.com"] #Email aniversario diario
        
        
        
        if nome_supervisor:
            if nome_supervisor not in self.supervisores:
                self.supervisores[nome_supervisor] = {"funcionarios": [], "email": email_supervisor}
            self.supervisores[nome_supervisor]["funcionarios"].append((nome_funcionario, mes_nascimento, dia_mes_nascimento,local))
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
        mes_seguinte = datetime.now() +  relativedelta(months=1)
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

        if aniversariantes:
            self._send_birthday_today_mail(aniversariantes, data_aniversario)                  
            self._send_mail_rh(aniversariantes_mes)
            self._send_birth_superior_mail(aniversariantes_mes)
                    
    def _send_birthday_today_mail(self, aniversariantes, data_aniversario):
        count = 0
        if  self.hoje in data_aniversario:
            count += 1
            email_morning = self.emailToday       #---------------------PRD-----------------------------
            # email_morning = self.email_teste    #---------------------QAS-----------------------------
            subject = f'Aniversariantes do dia'
            body = self._generate_dayling_email_body(aniversariantes)
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info(f'Lista de Aniversáriantes do dia Enviada')
            print(f'Aniversáriantes {count}')
            self._send_email(email_morning, subject, body)
        else: 
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info("Sem aniversáriantes no dia!")       

    def _send_mail_rh(self, aniversariantes_mes):
        mesStart = datetime.now().month
        diaFixo = 12
        data_fixa = datetime(datetime.now().year, mesStart, diaFixo)
        diaStart = (data_fixa.strftime("%d/%m"))
        hoje = datetime.now().strftime("%d/%m")
        if hoje == diaStart:
            # email_rh = self.email_teste  # ---------------------QAS-----------------------------
            email_rh = self.email_rh_list  # ---------------------PRD-----------------------------
            mes_atual = datetime.now() + relativedelta(months=1)
            mes_atual = mes_atual.strftime("%B").title()
            subject = f'Aniversariantes do mês de {mes_atual}'
            body = self._generate_rh_email_body(aniversariantes_mes)
            self._send_email(email_rh, subject, body)
            logging.info(f'Lista de Aniversáriantes do Mes de {mes_atual} Enviada para {email_rh}')

    def _send_birth_superior_mail(self, aniversariantes_mes): 
        count = 0
        hoje = datetime.now().strftime("%d/%m")
        mesStart = datetime.now().month
        diaFixo = 12   
        data_fixa = datetime(datetime.now().year, mesStart, diaFixo)
        diaStart = (data_fixa.strftime("%d/%m"))
        if hoje == diaStart:
            for supervisor, info in aniversariantes_mes.items(): 
                count += 1
                # emailSupervisor = self.email_teste    #---------------------QAS-----------------------------
                emailSupervisor = info["email"]       #---------------------PRD-----------------------------
                funcionarios = info["funcionarios"]     
                mes_atual = datetime.now() + relativedelta(months=1)
                mes_atual = mes_atual.strftime("%B").title()
                subject = f'Aniversariantes do mês de {mes_atual}' # Define o assunto do e-mail 
                body = self._generate_supervisor_email_body(supervisor, funcionarios) # Gera o corpo do e-mail 
                logging.info(f'Lista de Aniversáriantes de {supervisor} do mes de {mes_atual}')
                self._send_email(emailSupervisor, subject, body) # Envia o e-mail
    def _converter_data(self, data_str):
        return datetime.strptime(f"{data_str}/2024", "%d/%m/%Y")
    
    def _generate_rh_email_body(self, aniversariantes_mes):
        body = f"<strong>Olá Liderança. Segue a lista de colaboradores que fazem aniversário este mês:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += "<tr><th>Liderança</th><th>Colaboradores</th><th>Data</th><th>Setor</th></tr>"
        supervisores_ordenados = sorted(aniversariantes_mes.items())

        for supervisor, info in supervisores_ordenados:
            funcionarios_ordenados = sorted(info["funcionarios"], key=lambda x: self._converter_data(x[1]))
            for funcionario, dia_mes_nascimento, local in funcionarios_ordenados:
                body += f"<tr><td>{supervisor}</td><td>{funcionario}</td><td>{dia_mes_nascimento}</td><td>{local}</td></tr>"
        
        body += "</table><br>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body

    def _generate_dayling_email_body(self, aniversariantes):
        body = f"<strong>Olá Liderança. Segue a lista de colaboradores que fazem aniversário este mês:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += "<tr><th>Liderança</th><th>Colaboradores</th><th>Data</th><th>Setor</th></tr>"
        supervisores_ordenados = sorted(aniversariantes.items())
        for supervisor, info in supervisores_ordenados:
            # Adicionar um ano fictício para evitar ambiguidade e ordenar funcionários por data de aniversário
            funcionarios_ordenados = sorted(info["funcionarios"], key=lambda x: self._converter_data(x[1]))

            for funcionario, dia_mes_nascimento, local in funcionarios_ordenados:
                if dia_mes_nascimento == self.hoje:
                    body += f"<tr><td>{supervisor}</td><td>🎂{funcionario}</td><td>📅{dia_mes_nascimento}</td><td>{local}</td></tr>"              
        body += "</table><br>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_supervisor_email_body(self, supervisor, funcionarios):
        body = f"<strong>Olá {supervisor}. Segue a lista de colaboradores que fazem aniversário este mês:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += "<tr><th>Liderança</th><th>Colaboradores</th><th>Data</th><th>Setor</th></tr>"

        funcionarios_ordenados = sorted(funcionarios, key=lambda x: self._converter_data(x[1]))
        for funcionario, dia_mes_nascimento, local in funcionarios_ordenados:
                body += f"<tr><td>{supervisor}</td><td>{funcionario}</td><td>{dia_mes_nascimento}</td><td>{local}</td></tr>"
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