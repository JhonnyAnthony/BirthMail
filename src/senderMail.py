import requests
import json
import logging
from config import client_secret, client_id, tenant_id, scope, email_from,email_group

class Mail:
    def sendMail(nomeUsuario):
        email_group = [f"{nomeUsuario}@fgmdentalgroup.com"]
        subject = 'Hoje é o seu Aniversário - Parabéns!'
        body = f"""
                <html>
                    <body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                    <a href="https://fgmdentalgroup.com/Endomarketing/Aniversario/0001.html" style="display: flex; justify-content: center; align-items: center;">
                        <img src="https://i.imgur.com/klRdWw6.png" alt="ImageBirth">
                    </a>
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
