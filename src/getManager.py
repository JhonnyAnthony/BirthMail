import requests
from connectionDB import Database
from datetime import datetime
from config import client_secret, client_id, tenant_id, scope, email_from
import json
import logging
import locale

class Manager:
    def __init__(self):
        self.db_connection = Database()  # Inicializa a conexão com o banco de dados
        self.db_connection.connectData()  # Conecta ao banco de dados
        self.supervisores = {}  # Dicionário para armazenar supervisores e seus funcionários
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')  # Define a localidade para português do Brasil

    def connectionDB(self):
        db_results = self.db_connection.query()
        for data in db_results:
            self._process_user(data)  # Processa cada registro de funcionário

    def _process_user(self, data):
        nome_supervisor = self._format_name(data.NOMESUP)
        nome_funcionario = self._format_name(data.NOMFUN)
        data_nascimento = self._parse_date(data.DATNAS)
        self.email_rh = "jhonny.souza@fgmdentalgroup.com"
        usuario = data.USERSUP
        self.hoje = datetime.now().strftime("%d/%m")
        mes_nascimento = data_nascimento.strftime("%m")
        local = data.NOMLOCAL
        self.dia_mes_nascimento = data_nascimento.strftime("%d/%m")
        email_supervisor = f"jhonny.souza@fgmdentalgroup.com"  # Define o e-mail do supervisor para testes
        # email_supervisor = f"{usuario}@fgmdentalgroup.com"  # Define o e-mail do supervisor para testes
        if email_supervisor == 'bianca@fgmdentalgroup.com':
            email_supervisor == '' <-------
        if nome_supervisor:
            if nome_supervisor not in self.supervisores:
                self.supervisores[nome_supervisor] = {"funcionarios": [], "email": email_supervisor}
            self.supervisores[nome_supervisor]["funcionarios"].append((nome_funcionario, mes_nascimento, self.dia_mes_nascimento,local))

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
            for funcionario, mes_nascimento, self.dia_mes_nascimento, local in info["funcionarios"]:
                if mes_nascimento == mes_atual:
                    if supervisor not in aniversariantes:
                        aniversariantes[supervisor] = {"funcionarios": [], "email": info["email"]}
                    aniversariantes[supervisor]["funcionarios"].append((funcionario, self.dia_mes_nascimento,local))
        return aniversariantes

    def birthMounth(self):
        aniversariantes = self.filtrar_aniversariantes_do_mes()

        if aniversariantes:
            self._send_mail_rh(aniversariantes)
            self._send_birth_superior_mail(aniversariantes)
            self._send_birthday_morning_mail(aniversariantes)

    def _send_birthday_morning_mail(self, aniversariantes): 
        for supervisor, info in aniversariantes.items(): 
            email_rh = self.email_rh # Obtém o e-mail do supervisor 
            funcionarios = info["funcionarios"] 
            subject = f'Aniversariantes do dia' # Define o assunto do e-mail 
            body = self._generate_dayling_email_body(supervisor, funcionarios) # Gera o corpo do e-mail 
            if self.dia_mes_nascimento == self.hoje:
                print(f"E-mail enviado a {supervisor} ({email_rh})") 
                self._send_email(email_rh, subject, body) # Envia o e-mail

    def _send_birth_superior_mail(self, aniversariantes): 
        for supervisor, info in aniversariantes.items(): 
            emailSupervisor = info["email"] # Obtém o e-mail do supervisor 
            funcionarios = info["funcionarios"] 
            mes_atual = datetime.now().strftime("%B").title() 
            subject = f'Aniversariantes do mês de {mes_atual}' # Define o assunto do e-mail 
            body = self._generate_supervisor_email_body(supervisor, funcionarios) # Gera o corpo do e-mail 
            # print(f"E-mail enviado a {supervisor} ({emailSupervisor})") 
            # self._send_email(emailSupervisor, subject, body) # Envia o e-mail
            
    def _send_mail_rh(self, aniversariantes):
        email_rh = self.email_rh 
        mes_atual = datetime.now().strftime("%B").title()
        subject = f'Aniversariantes do mês de {mes_atual}'
        body = self._generate_rh_email_body(aniversariantes)
        # print(f"E-mail enviado ao RH ({email_rh})")
        # self._send_email(email_rh, subject, body)

    def _generate_rh_email_body(self, aniversariantes):
        body = "Olá. Segue a lista de funcionários que fazem aniversário este mês:<br><br>"
        for supervisor, info in aniversariantes.items():
            body += f"Supervisor: {supervisor}<br>"
            for funcionario, self.dia_mes_nascimento,local in info["funcionarios"]:
                body += f" 🎂{funcionario}, 📅{self.dia_mes_nascimento}, {local}<br>"
            body += "<br>"
        body += "Atenciosamente,<br>Equipe de Recursos Humanos"
        return body
    
    def _generate_dayling_email_body(self, supervisor, funcionarios):
        body = f"Olá {supervisor}. Segue a lista de funcionários que fazem aniversário hoje:<br><br>"
        for funcionario, self.dia_mes_nascimento,local in funcionarios:
            if self.dia_mes_nascimento == self.hoje:
                body += f" 🎂{funcionario}, 📅{self.dia_mes_nascimento}, {local}<br>"
        body += "<br>Atenciosamente,<br>Equipe de Recursos Humanos"
        return body

    def _generate_supervisor_email_body(self, supervisor, funcionarios):
        body = f"Olá {supervisor}. Segue a lista de funcionários que fazem aniversário este mês:<br><br>"
        for funcionario, self.dia_mes_nascimento,local in funcionarios:
            body += f" 🎂{funcionario}, 📅{self.dia_mes_nascimento}, {local}<br>"
        body += "<br>Atenciosamente,<br>Equipe de Recursos Humanos"
        return body

    def _send_email(self, email_to, subject, body):
        email_group = [email_to]
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

if __name__ == "__main__":
    manager = Manager()
    manager.connectionDB()
    manager.birthMounth()
