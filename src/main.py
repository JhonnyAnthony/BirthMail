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
        resultados = self.db.query() #Armazena dados dos Usuários
        seen = set()  # Conjunto para rastrear nomes de usuários únicos

        for resultado in resultados: #Loop para verificar todos os Usuários
            # tipoAdm = resultado.TIPADM                #NÃO UTILIZADO
            # numeroEmp = resultado.NUMEMP              #NÃO UTILIZADO
            # tipoCol = resultado.TIPCOL                #NÃO UTILIZADO
            # sitaFa = resultado.SITAFA                 #NÃO UTILIZADO
            numCad = resultado.NUMCAD                   #Armazenamento da Matricula
            nomeFun = resultado.NOMFUN                  #Utilizado para Conversão 
            self.nomeCompleto = nomeFun.title()         #Armazenamento da Nome Completo do Usuário
            dataNas = resultado.DATNAS                  #Armazenamento da Data de Nascimento
            self.emailPessoal = resultado.EMAPAR        #Armazenamento do E-mail do Usuário
            self.nomeUsuario = resultado.NOMUSU         #Armazenamento do Usuário de E-mail.
            hoje = datetime.now().strftime("%d/%m")     #Armazenamento da Data do Dia
            if not isinstance(dataNas, datetime):       #Situação para poder mudar a tipagem da data
                dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")   #Armazenamento de dado para Conversão
            data_nascimento = dataNas.strftime("%d/%m") #Armazenamento de Data de Nascimento pós Conversão
# 
            if (data_nascimento == hoje):               #Situação quando Data Nascimento é IGUAL Data do Dia
            # if (self.nomeUsuario=='gabriel.natan' or self.nomeUsuario=='adriano.guerra' or self.nomeUsuario=='jhonny.souza'): #TESTE
                if (self.nomeUsuario not in seen and self.emailPessoal != ' '):# Situação para não duplicar nomes
                    seen.add(self.nomeUsuario) #Adiciona nome aos dados "Vistos"
                    print(data_nascimento,self.nomeUsuario,self.emailPessoal,numCad) #Print de Retorno de dados
                    # BithMail.sendMail(self)  # Chama a funcao do envio do email   
        return self.nomeUsuario,self.emailPessoal,self.nomeCompleto # Retorno de dados

    def sendMail(self): #Faz envio do E-mail
        email_group = [f"{self.nomeUsuario}@fgmdentalgroup.com",f'{self.emailPessoal}'] #Armazenamento dos E-mails a serem enviados
        # email_group = [f"jhonny.souza@fgmdentalgroup.com"] # TESTE

        subject = f'Hoje é o seu Aniversário - Parabéns {self.nomeCompleto}!' #Titulo do E-mail
        picture = 'https://fgmdentalgroup.com/wp-content/uploads/2025/01/aniversario-1.jpg' #Armazena a imagem do E-mail
        linkRedirect= 'https://fgmdentalgroup.com/Endomarketing/Aniversario/0001.html'      #Armazena o link de redirecionamento da Imagem
        #Corpo do E-mail 
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
        # Obter token de acesso
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token' #End-point
        data = { #Dados de requisição API
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope
        }
        response = requests.post(url, data=data) #Armazenamento da situação da API
        token = response.json().get('access_token') #Armazena o Acess token

        # Preparar lista de destinatários
        to_recipients = [{'emailAddress': {'address': email}} for email in email_group]

        # Enviar email
        url = f'https://graph.microsoft.com/v1.0/users/{email_from}/sendMail' #End-Point de envio de e-mail
        headers = { #Dados de vericação e autorização da API
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        email_msg = { #JSON de envio de e-mail
            'message': {
                'subject': subject,
                'body': {
                    'contentType': 'HTML',
                    'content': body
                },
                'toRecipients': to_recipients
            }
        }
        response = requests.post(url, headers=headers, data=json.dumps(email_msg))#Armazena situação do E-mail
        if response.status_code == 202:
            logging.info(f"Enviado e-mail para {email_group}")
        else:
            logging.error(f'Falha ao enviar email: {response.status_code}: {response.text}')

if __name__ == "__main__": #Inicia o Projeto
    main = BithMail()
    main.send_birthday_emails()
    start = Database()
    start.connectData()
    start.query()