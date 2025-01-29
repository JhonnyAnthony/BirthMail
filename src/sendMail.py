from datetime import datetime
from connectionDB import Database
from config import client_secret, client_id, tenant_id, scope, email_from, pictureBirth, pictureNew, linkRedirect
import requests
import logging
import json

class SendMail:
    def __init__(self):
        self.db = Database()
        self.db.connectData()
    
    def send_birthday_emails(self):
        resultados = self.db.query()  # Armazena dados dos Usuários
        seen = set()  # Conjunto para rastrear nomes de usuários únicos
        for resultado in resultados:  # Loop para verificar todos os Usuários
            self._process_user(resultado, seen)

    def _process_user(self, resultado, seen):
        nomeSuperior = resultado.NOMESUP
        datAdm = resultado.DATADM
        nomeFun = resultado.NOMFUN


        if nomeSuperior and nomeFun:
            self.nomeSup = nomeSuperior.title()
            self.nomeCompleto = nomeFun.title()

        numCad = resultado.NUMCAD
        dataNas = resultado.DATNAS
        self.nomeUsuario = resultado.NOMUSU
        hoje = datetime.now().strftime("%d/%m")
        hojeAdm = datetime.now().strftime("%d/%m/%y")

        if not isinstance(dataNas, datetime):
            datAdm = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
            dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")

        data_admissao = datAdm.strftime("%d/%m/%y")
        data_nascimento = dataNas.strftime("%d/%m")
        self.emailPessoal = resultado.EMAPAR
        self.email_corporativo = f"{self.nomeUsuario}@fgmdentalgroup.com"


        if data_admissao == hojeAdm:
            self._send_anniversary_email(seen)
            print(self.nomeCompleto,data_admissao)
        if data_nascimento == hoje:
            self._send_birthday_email(seen)
            print(self.nomeCompleto,data_admissao)

    def _send_anniversary_email(self, seen):
        if self.nomeUsuario not in seen and self.emailPessoal.strip():
            seen.add(self.nomeUsuario)
            self.subject = 'teste!'
            self.body = self._generate_email_body(pictureNew, 'ImageBirth')
            logging.info(f"E-mail enviado a {self.nomeUsuario}")
            self._send_email()

    def _send_birthday_email(self, seen):
        if self.nomeUsuario not in seen and self.emailPessoal.strip():
            seen.add(self.nomeUsuario)
            self.subject = f'Hoje é o seu Aniversário - Parabéns {self.nomeCompleto}!'
            self.body = self._generate_email_body(pictureBirth, 'ImageBirth', linkRedirect)
            logging.info(f"E-mail enviado a {self.nomeUsuario}")
            self._send_email()

    def _generate_email_body(self, image_src, alt_text, link=None):
        if link:
            return f"""<html><br><body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                        <a href="{link}" style="display: flex; justify-content: center; align-items: center;">
                            <img src="{image_src}" alt="{alt_text}">
                        </a></body></html>"""
        else:
            return f"""<html><br><body style="display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0;">
                        <a style="display: flex; justify-content: center; align-items: center;">
                            <img src="{image_src}" alt="{alt_text}">
                        </a></body></html>"""

    def _send_email(self):
        # email_group = [f"{self.email_corporativo}",f"{self.emailPessoal}"]  # PRD
        email_group = [f"jhonny.souza@fgmdentalgroup.com"]  # TESTE
        subject = self.subject
        body = self.body

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

        if response.status_code == 202:
            logging.info(f"Enviado e-mail para {email_group}")
        else:
            logging.error(f'Falha ao enviar email: {response.status_code}: {response.text}')
