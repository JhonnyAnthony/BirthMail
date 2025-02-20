import requests
from connectionDB import Database
from datetime import datetime
from dateutil.relativedelta import relativedelta
from config import client_secret, client_id, tenant_id, scope, email_from
import json
import logging
import locale

class TempoCasa:
    def __init__(self):
        self.db_connection = Database()  # Inicializa a conexão com o banco de dados
        self.db_connection.connectData()  # Conecta ao banco de dados
        self.supervisores = {}  # Dicionário para armazenar supervisores e seus funcionários
        locale.setlocale(locale.LC_TIME, 'pt_BR')  # Define a localidade para português do Brasil

    def connectionDB(self):
        db_results = self.db_connection.query_principal()
        for data in db_results:
            self._process_user(data)  # Processa cada registro de funcionário

    def _process_user(self, data):
        data_adm = self._parse_date(data.DATADM)
        ano_adm = self._parse_date(data.DATADM)
        ano_dem = self._parse_date(data.DATADM)
        self.situacao = data.SITAFA
        self.usuario = data.NOMUSU
        self.nomeCompleto = self._format_name(data.NOMFUN)
        self.email_pessoal = data.EMAPAR
        self.data_admissao = data_adm.strftime("%d/%m")
        self.ano_admissao = ano_adm.strftime("%Y")
        self.ano_demissao = ano_dem.strftime("%Y")
        self.ano_atual = datetime.now().strftime("%Y")
        self.hoje = datetime.now().strftime("%d/%m")
        self.email_teste = ["jhonny.souza@fgmdentalgroup.com"]  # -------------------------- QAS ------------------------
        data_dem = self._parse_date(data.DATAFA)
        self.data_demissao = data_dem.strftime("%d/%m/%Y")
        if self.data_demissao == '31/12/1900':
            breakpoint
        data_demissao_datetime = datetime.strptime(self.data_demissao, "%d/%m/%Y")
        # Subtrair 6 meses
        seisMeses = data_demissao_datetime - relativedelta(months=6)
        teste = seisMeses.strftime('%d/%m/%Y')
        # if self.data_demissao <= teste:
            # print(f"teste, {self.nomeCompleto}")
        if self.data_admissao == self.hoje and self.situacao == 1:
            self.anoCasa = int(self.ano_atual) - int(self.ano_admissao)
            
            funcoes = {
                5: self.filtrar_aniversariantes_5_anos,
                10: self.filtrar_aniversariantes_10_anos,
                15: self.filtrar_aniversariantes_15_anos,
                20: self.filtrar_aniversariantes_20_anos,
                25: self.filtrar_aniversariantes_25_anos,
                30: self.filtrar_aniversariantes_30_anos
            }
            
            funcao = funcoes.get(self.anoCasa)
            if funcao:
                funcao()
            else:
                self.filtrar_aniversariantes()
                # print(anoCasa)
                # se for aniversário de empresa irá jogar para os filtros, para saber qual é

        
    def _format_name(self, name):
        return ' '.join([word.capitalize() for word in name.split()]) if name else ""

    def _parse_date(self, date_str):
        if not isinstance(date_str, datetime):
            return datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
        return date_str

   
    def filtrar_aniversariantes(self):
        self._send_mail_year    
        print(f"aniversário de empresa DE {self.nomeCompleto} completa {self.anoCasa} anos")

    def filtrar_aniversariantes_5_anos(self):
        self._send_mail_5_year
        print(f"aniversário de empresa DE 5 {self.nomeCompleto}")

            # joga para o body de tempo de empresa
    def filtrar_aniversariantes_10_anos(self):
        self._send_mail_10_year
        print(f"aniversário de empresa DE 10 {self.nomeCompleto}")
            # joga para o body de tempo de empresa
    def filtrar_aniversariantes_15_anos(self):
        self._send_mail_15_year
        print(f"aniversário de empresa DE 15 {self.nomeCompleto}")
            # joga para o body de tempo de empresa
    def filtrar_aniversariantes_20_anos(self):
        self._send_mail_20_year
        print(f"aniversário de empresa DE 20 {self.nomeCompleto}")
            # joga para o body de tempo de empresa
    def filtrar_aniversariantes_25_anos(self):
        self._send_mail_25_year
        print(f"aniversário de empresa DE 25 {self.nomeCompleto}")
            # joga para o body de tempo de empresa
    def filtrar_aniversariantes_30_anos(self):
        self._send_mail_30_year
        print(f"aniversário de empresa DE 30{self.nomeCompleto}")
            # joga para o body de tempo de empresa
        
    
    def filtrar_datas(self):
        datas = []
        # for supervisor, info in aniversariantes.items():
        #     for funcionario in info["funcionarios"]:
        #         datas.append(funcionario[1])  # Adiciona a data de aniversário
        # return datas
    

                    
    def _send_mail_year(self):
        print()
    def _send_mail_5_year(self):
        print("estrela")
    def _send_mail_10_year(self):
        print("estrela")
    def _send_mail_15_year(self):
        print("estrela")
    def _send_mail_20_year(self):
        print("estrela")
    def _send_mail_25_year(self):
        print("estrela")
    def _send_mail_30_year(self):
        print("estrela")
    
    
    def _generate_1_year_body(self):
        body = f"<strong>Aniversário 1 ano de empresa<br><br></strong>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_5_year_body(self):
        body = f"<strong>Aniversário 5 ano de empresa<br><br></strong>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_10_year_body(self):
        body = f"<strong>Aniversário 10 ano de empresa<br><br></strong>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_15_year_body(self):
        body = f"<strong>Aniversário 15 ano de empresa<br><br></strong>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_20_year_body(self):
        body = f"<strong>Aniversário 20 ano de empresa<br><br></strong>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_25_year_body(self):
        body = f"<strong>Aniversário 25 ano de empresa<br><br></strong>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
    def _generate_30_year_body(self):
        body = f"<strong>Aniversário 30 ano de empresa<br><br></strong>"
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
if __name__ == "__main__":
    manager = TempoCasa()
    manager.connectionDB()