import os
import json
import logging
import urllib3
import requests
from connectionDB import Database
from datetime import datetime
from config import client_secret,client_id,tenant_id,scope,email_from
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
db = Database()
resultados = db.query()
class BithMail:
    def __init__(self):
        self.service_ticket = None
        self.key_password = None
        self.id_code = None
    
    def logs():
        # Define the directory path where logs will be stored
        log_directory = r"~/GitHub/BirthMail/Logs"
            # Create the log directory if it doesn't exist
        if not os.path.exists(log_directory):
                os.makedirs(log_directory)

            # Get the current date and time
        current_datetime = datetime.now()

                # Generate a filename based on the current date within the log folder
        log_filename = os.path.join(log_directory, current_datetime.strftime("%Y-%m-%d") + "_log.log")

                # Configure logging to output to this filename
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_filename  # Use the generated filename within the log folder
        )           
    
    def filter():
        for resultado in resultados:
            tipoAdm = resultado.TIPADM #tipo adm???
            numeroEmp = resultado.NUMEMP #numero emp????
            tipoCol = resultado.TIPCOL # tipo col???
            nomeFun = resultado.NOMFUN # nume Completo
            sitaFa = resultado.SITAFA #situacao 
            matricula = resultado.CODUSU #matricula
            dataNas = resultado.DATNAS #data nascimento
            nomeUsuario = resultado.NOMUSU #usuario
            emailPessoal = resultado.EMAPAR #email pessoal
            hoje = datetime.now()
            # Verificar o tipo de dataNas
            if isinstance(dataNas, datetime):
                dataNass = dataNas
            
            else:
                dataNass = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
            # Formatar as datas
            data_hoje = hoje.strftime("%d/%m")
            data_nascimento = dataNass.strftime("%d/%m")
            if (data_nascimento == data_hoje):
                start.sendMail()
            else:
                logging.info("Não tem ninguem de aniversário hoje")
        
    def sendMail(self):
        email_group = ['jhonny.souza@fgmdentalgroup.com']
        #email_group = ['guest@fgm.ind.br','infra@fgm.ind.br']
        
        subject = 'Hoje é o seu Aniversário - Parabéns!'
        body = f"""
                <html>
                    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                    <a href="https://fgmdentalgroup.com/Endomarketing/Aniversario/0001.html" style="display: flex; justify-content: center; align-items: center;">
                        <img src="https://i.imgur.com/klRdWw6.png" alt="ImageBirth">
                    </a>
                </html>
                """

        # Obter token de acesso
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'

        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope
        }
        response = requests.post(url, data=data)
        token = response.json().get('access_token')

        # Preparar lista de destinatários
        to_recipients = [{'emailAddress': {'address': email}} for email in email_group]

        # Enviar email
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
        print(response.text)
        if response.status_code == 202:
            logging.info(f"Enviado e-mail para{email_group}")
        else:
            logging.error(f'Falha ao enviar email: {response.status_code}: {response.text}')   
        


if __name__ == "__main__":
    start = BithMail()
    
