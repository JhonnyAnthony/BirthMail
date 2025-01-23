from datetime import datetime
from connectionDB import Database
from config import client_secret, client_id, tenant_id, scope, email_from
import requests
import logging
import json
class SendMail:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def send_birthday_emails(self):
        resultados = self.db.query() #Armazena dados dos Usuários
        seen = set()  # Conjunto para rastrear nomes de usuários únicos
        for resultado in resultados: #Loop para verificar todos os Usuários
            nomeSuperior = resultado.NOMESUP
            nomeFun = resultado.NOMFUN                  #Utilizado para Conversão 
            self.userSup = resultado.USERSUP
            setor = resultado.NOMLOC
            self.local = resultado.NUMLOC
            self.posto = resultado.POSTRA_CHE
            if nomeSuperior and nomeFun and setor:
                self.setor = setor.title()
                self.nomeSup = nomeSuperior.title()
                self.nomeCompleto = nomeFun.title()         #Armazenamento da Nome Completo do Usuário
            # userSup = resultado.USERSUP
            numCad = resultado.NUMCAD                   #Armazenamento da Matricula
            dataNas = resultado.DATNAS                  #Armazenamento da Data de Nascimento
            self.emailPessoal = resultado.EMAPAR        #Armazenamento do E-mail do Usuário
            self.nomeUsuario = resultado.NOMUSU         #Armazenamento do Usuário de E-mail.
            mes = datetime.now().strftime("%m")     #Armazenamento da Data do Dia
            if not isinstance(dataNas, datetime):       #Situação para poder mudar a tipagem da data
                dataNas = datetime.strptime(dataNas, "%Y-%m-%d %H:%M:%S")   #Armazenamento de dado para Conversão
            data_nascimento = dataNas.strftime("%m") #Armazenamento de Data de Nascimento pós Conversão
            # if (data_nascimento == mes):               #Situação quando Data Nascimento é IGUAL Data do Dia
            idePos = resultado.IDEPOS
            teste = [self.local,nomeSuperior, idePos]
            posto = [self.nomeCompleto, self.posto,nomeSuperior,idePos,self.userSup, setor]
            superior = []
            if (data_nascimento == mes): #TESTE
                if (superior):
                    print(nomeFun)
                if (self.posto not in seen and self.emailPessoal != ' ' and nomeSuperior != None):# Situação para não duplicar nomes
                    seen.add(self.nomeUsuario) #Adiciona nome aos dados "Vistos"
                    posto = [self.nomeUsuario, data_nascimento,nomeSuperior]
                    # SendMail.sendMail(self)  # Chama a funcao do envio do email   
        return self.nomeUsuario,data_nascimento,self.nomeCompleto,self.userSup # Retorno de dados
    def sendMail(self): #Faz envio do E-mail
        email_group = [f"{self.userSup}@fgmdentalgroup.com"] #Armazenamento dos E-mails a serem enviados
        email_group = [f"jhonny.souza@fgmdentalgroup.com"] # TESTE

        subject = f'Aniversáriantes do mês, Setor {self.setor}!' #Titulo do E-mail
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
if __name__ == "__main__":
    start = SendMail()
    send = start.send_birthday_emails()