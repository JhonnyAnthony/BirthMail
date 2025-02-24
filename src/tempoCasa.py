from connectionDB import Database
from datetime import datetime, timedelta
import locale
from config import client_secret, client_id, tenant_id, scope, email_from
import requests
import logging
import json
class TempoCasa:
    def __init__(self):
        self.db_connection = Database()
        self.db_connection.connectData()
        self.data = {}
        locale.setlocale(locale.LC_TIME, 'pt_BR')

    def connectionDB(self):
        db_results = self.db_connection.query_tempoCasa()
        for data in db_results:
            self._process_user(data)

    def _process_user(self, data):
        data_adm = self._parse_date(data.DATADM).strftime("%d/%m/%Y")
        data_dem = self._parse_date(data.DATAFA).strftime("%d/%m/%Y") if data.DATAFA != datetime(1900, 12, 31) else datetime.now().strftime("%d/%m/%Y")
        cpf = data.NUMCPF

        if cpf not in self.data:
            self.data[cpf] = {
                'nome': data.NOMFUN,
                'situacao': data.SITAFA,
                'matriculas': [],
                'email_pessoal': data.EMAPAR,
                'email_corporativo': data.EMACOM,
                'admissoes': []
            }

        self.data[cpf]['matriculas'].append((data_adm, data_dem))
        self.data[cpf]['admissoes'].append((data_adm, data_dem))

        if data.SITAFA == 1:
            self._check_anniversary(cpf, data.NOMFUN, data_adm)

    def _check_anniversary(self, cpf, nome, data_adm):
        tempo_de_casa = self.calcular_tempo_de_casa(self.data[cpf]['admissoes'])
        data_atual = datetime.now()
        hoje = datetime.now().strftime("%d/%m/%Y")
        primeiro_dia_proximo_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
        ultimo_dia_mes_atual = primeiro_dia_proximo_mes - timedelta(days=1)
        ultimodia = int(ultimo_dia_mes_atual.strftime('%d'))
        anos = tempo_de_casa.days // 365
        meses = (tempo_de_casa.days % 365) // ultimodia

        # print(f"Aniversário de empresa de {nome.title()} de {anos} {'anos' if anos > 1 else 'ano'} e {meses} {'meses' if meses > 1 else 'mes'} | Data de Admissao: {data_adm}")
        if anos >= 1 and data_adm == '03/06/2024':
            print(f"Aniversário de empresa de {nome.title()} de {anos} {'anos' if anos > 1 else 'ano'} e {meses} {'meses' if meses > 1 else 'mes'} | Data de Admissao: {data_adm}")
            self._apply_filters(anos, self.data[cpf])

    def _apply_filters(self, anos, info):
        funcoes = {
            5: self.filtrar_aniversariantes_5_anos,
            10: self.filtrar_aniversariantes_10_anos,
            15: self.filtrar_aniversariantes_15_anos,
            20: self.filtrar_aniversariantes_20_anos,
            25: self.filtrar_aniversariantes_25_anos,
            30: self.filtrar_aniversariantes_30_anos
        }

        funcao = funcoes.get(anos, self.filtrar_aniversariantes)
        funcao(info,anos)
    def calcular_tempo_de_casa(self, admissoes):
        admissoes.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
        if len(admissoes) > 1:
            data_demissao_antiga = datetime.strptime(admissoes[-2][1], "%d/%m/%Y")
            data_admissao_nova = datetime.strptime(admissoes[-1][0], "%d/%m/%Y")
            diferenca_tempo = data_admissao_nova - data_demissao_antiga

            if diferenca_tempo < timedelta(days=180):
                data_admissao_antiga = datetime.strptime(admissoes[-2][0], "%d/%m/%Y")
                return datetime.now() - data_admissao_antiga
            else:
                return datetime.now() - data_admissao_nova
        else:
            data_admissao = datetime.strptime(admissoes[0][0], "%d/%m/%Y")
            return datetime.now() - data_admissao

    def _parse_date(self, date_str):
        return date_str if isinstance(date_str, datetime) else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def filtrar_aniversariantes(self, info, anos):
        self._send_mail_year()
        print(f"Aniversário de empresa de {info['nome'].title()} completa {anos} {'anos' if anos > 1 else 'ano'}")

    def filtrar_aniversariantes_5_anos(self, info):
        self._send_mail_5_year()
        print(f"Aniversário de empresa de 5 anos de {info['nome'].title()}")

    def filtrar_aniversariantes_10_anos(self, info):
        self._send_mail_10_year()
        print(f"Aniversário de empresa de 10 anos de {info['nome'].title()}")

    def filtrar_aniversariantes_15_anos(self, info):
        self._send_mail_15_year()
        print(f"Aniversário de empresa de 15 anos de {info['nome'].title()}")

    def filtrar_aniversariantes_20_anos(self, info):
        self._send_mail_20_year()
        print(f"Aniversário de empresa de 20 anos de {info['nome'].title()}")

    def filtrar_aniversariantes_25_anos(self, info):
        self._send_mail_25_year()
        print(f"Aniversário de empresa de 25 anos de {info['nome'].title()}")

    def filtrar_aniversariantes_30_anos(self, info):
        self._send_mail_30_year()
        print(f"Aniversário de empresa de 30 anos de {info['nome'].title()}")

    def _send_mail_year(self):
        print("Enviando email de aniversário de empresa")

    def _send_mail_5_year(self):
        print("Enviando email de 5 anos de empresa")

    def _send_mail_10_year(self):
        print("Enviando email de 10 anos de empresa")

    def _send_mail_15_year(self):
        print("Enviando email de 15 anos de empresa")

    def _send_mail_20_year(self):
        print("Enviando email de 20 anos de empresa")

    def _send_mail_25_year(self):
        print("Enviando email de 25 anos de empresa")

    def _send_mail_30_year(self):
        print("Enviando email de 30 anos de empresa")
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
    start = TempoCasa()
    start.connectionDB()