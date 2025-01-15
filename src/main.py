import os
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
        log_directory = r"/home/fgm/Scripts/BirthMail/Logs"
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
        seen = set()  # Conjunto para rastrear nomes de usuários únicos

        for resultado in resultados:
            tipoAdm = resultado.TIPADM
            numeroEmp = resultado.NUMEMP
            tipoCol = resultado.TIPCOL
            sitaFa = resultado.SITAFA
            numCad = resultado.NUMCAD
            matricula = resultado.CODUSU
            nomeFun = resultado.NOMFUN
            self.nomeCompleto = nomeFun.title()
            dataNas = resultado.DATNAS
            self.emailPessoal = resultado.EMAPAR
            hoje = datetime.now().strftime("%d/%m")
            self.nomeUsuario = resultado.NOMUSU

            if not isinstance(dataNas, datetime):
                dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
            data_nascimento = dataNas.strftime("%d/%m")
# 
            if (data_nascimento == hoje):
            # if (self.nomeUsuario=='gabriel.natan' or self.nomeUsuario=='adriano.guerra' or self.nomeUsuario=='jhonny.souza'):
                if (self.nomeUsuario not in seen and self.emailPessoal != ' '):# if para nao duplicar nomes
                    seen.add(self.nomeUsuario)
                    # seen.add(self.emailPessoal)
                    print(data_nascimento,self.nomeUsuario,self.emailPessoal,numCad)
                    BithMail.sendMail(self)  # Chama a funcao do envio do email
            # print(data_nascimento, numCad, self.nomeUsuario,self.emailPessoal)  
                
        return self.nomeUsuario,self.emailPessoal,self.nomeCompleto

    def sendMail(self):
        email_group = [f"{self.nomeUsuario}@fgmdentalgroup.com",f'{self.emailPessoal}']
        # email_group = [f"jhonny.souza@fgmdentalgroup.com"] 

        subject = f'Hoje é o seu Aniversário - Parabéns {self.nomeCompleto}!'
        picture = 'https://fgmdentalgroup.com/wp-content/uploads/2025/01/aniversario-1.jpg'
        linkRedirect= 'https://fgmdentalgroup.com/Endomarketing/Aniversario/0001.html'
        body = f"""
                <html>
                    <br>
                    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                        <a href="{linkRedirect}" style="display: flex; justify-content: center; align-items: center;">
                            <img src="{picture}" alt="ImageBirth">
                        </a>
                    </body>
                </html>
                """
        # subject = 'TESTE'

        # body = f"""
        #         <html>
        #             <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
        #                 <h1>teste</h1>
        #             </body>
        #         </html>
        #         """

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