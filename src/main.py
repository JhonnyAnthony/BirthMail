import os
import logging
import json
import logging
import requests

from datetime import datetime
from connectionDB import Database
from config import client_secret, client_id, tenant_id, scope, email_from

class BithMail:
    def __init__(self):
        self.db = Database()
        self.db.connectData()
    @staticmethod
    def logs():
        log_directory = r"C:/Scripts/BirthMail/Logs"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        current_datetime = datetime.now()
        log_filename = os.path.join(log_directory, current_datetime.strftime("%Y-%m-%d") + "_log.log")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_filename
        )
    logs()

    def send_birthday_emails(self):
        resultados = self.db.query()

        for resultado in resultados:
            tipoAdm = resultado.TIPADM #tipo adm???
            numeroEmp = resultado.NUMEMP #numero emp????
            tipoCol = resultado.TIPCOL # tipo col???
            nomeFun = resultado.NOMFUN # nume Completo
            sitaFa = resultado.SITAFA #situacao 
            numCad= resultado.NUMCAD
            matricula = resultado.CODUSU #matricula
            dataNas = resultado.DATNAS #data nascimento
            emailPessoal = resultado.EMAPAR #email pessoal
            hoje = datetime.now().strftime("%d/%m")
            self.nomeUsuario = resultado.NOMUSU #usuario
            if not isinstance(dataNas, datetime):
                dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
            data_nascimento = dataNas.strftime("%d/%m")
            # print(data_nascimento)
            # if (data_nascimento == hoje):
            #     print(data_nascimento,self.nomeUsuario)
                # BithMail.sendMail(self)  
            print(data_nascimento, numCad, self.nomeUsuario)    
            
        return self.nomeUsuario

    def sendMail(self):
        # email_group = [f"{self.nomeUsuario}@fgmdentalgroup.com"]
        email_group = [f"jhonny.souza@fgmdentalgroup.com"]

        # subject = 'TESTE'
        # body = f"""
        #         <html>
        #             <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
        #             <a href="https://fgmdentalgroup.com/Endomarketing/Aniversario/0001.html" style="display: flex; justify-content: center; align-items: center;">
        #                 <img src="https://i.imgur.com/klRdWw6.png" alt="ImageBirth">
        #             </a>
        #         </html>
        #         """
        subject = 'TESTE'

        body = f"""
                <html>
                    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                        <h1>teste</h1>
                    </body>
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
            logging.info(f"Enviado e-mail para {email_group}")
        else:
            logging.error(f'Falha ao enviar email: {response.status_code}: {response.text}')

if __name__ == "__main__":
    main = BithMail()
    main.send_birthday_emails()
    start = Database()
    start.connectData()
    start.query()