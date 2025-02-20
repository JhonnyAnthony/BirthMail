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
        resultados = self.db.query_principal()  # Armazena dados dos Usuários
        seen = set()  # Conjunto para rastrear nomes de usuários únicos
        for resultado in resultados:  # Loop para verificar todos os Usuários
            self._process_user(resultado,seen)


    def _process_user(self, resultado,seen):
        datAdm = resultado.DATADM
        nomeFun = resultado.NOMFUN
        RN = resultado.RN
        if nomeFun:

            self.nomeCompleto = nomeFun.title()
        situacao = resultado.SITAFA
        numCad = resultado.NUMCAD
        dataNas = resultado.DATNAS
        self.nomeUsuario = resultado.NOMUSU
        # print(self.nomeUsuario)
        hoje = datetime.now().strftime("%d/%m")
        hojeAdm = datetime.now().strftime("%d/%m/%y")

        if not isinstance(dataNas, datetime):
            datAdm = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
            dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")
        
        data_admissao = datAdm.strftime("%d/%m/%y")
        data_nascimento = dataNas.strftime("%d/%m")
        aniversarianteMes = dataNas.strftime("%m")
        mes = datetime.now().strftime("%m")
        self.emailPessoal = resultado.EMAPAR
        self.email_corporativo = f"{self.nomeUsuario}@fgmdentalgroup.com"

        if data_admissao == hojeAdm:
            logging.info("--------------Informações de Bem Vindo--------------")
            # logging.info(f"Bem Vindo {self.nomeCompleto}")
            # self._send_welcome_mail(seen)
        # elif data_nascimento == hoje and self.nomeUsuario == 'daniel.lucas':
        elif data_nascimento == hoje:
            logging.info("--------------Informações de Aniversário--------------")
            logging.info(f"Hoje é o Aniversário de {self.nomeCompleto}")
            print(F"{self.nomeCompleto}, ({self.emailPessoal}), {situacao}, {RN}")
            # self._send_birthday_email(seen)


    def _send_welcome_mail(self, seen):
        if self.nomeUsuario not in seen and self.emailPessoal.strip():
            seen.add(self.nomeUsuario)
            email = [f"{self.email_corporativo}",f"{self.emailPessoal}"]  # ---------------------PRD-----------------------------
            # email = ["jhonny.souza@fgmdentalgroup.com"] # ---------------------QAS-----------------------------
            subject = f'Seja Bem-Vindo(a) {self.nomeCompleto}!'
            body = self._generate_email_body(pictureNew, 'ImageWelcome')
            # self._send_email(email,subject,body)


    def _send_birthday_email(self, seen):
        if self.emailPessoal == ' ':
            self.emailPessoal = self.email_corporativo
        if self.nomeUsuario not in seen and self.emailPessoal.strip():
            seen.add(self.nomeUsuario)
            email = [f"{self.email_corporativo}",f"{self.emailPessoal}"] # ---------------------PRD-----------------------------
            # email = ["jhonny.souza@fgmdentalgroup.com"] # ---------------------QAS-----------------------------
            seen.add(self.nomeUsuario)
            subject = f'Feliz Aniversário {self.nomeCompleto}!'

            body = self._generate_email_body(pictureBirth, 'ImageBirth', linkRedirect)
            self._send_email(email,subject,body)

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

    def _send_email(self,email_, subject,body):
        email_group = email_  

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
            logging.info("------------------------------------------------------------------------------------")

        else:
            logging.error(f'Falha ao enviar email: {response.status_code}: {response.text}')
