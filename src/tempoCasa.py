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
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')


    def connectionDB(self):
        db_results = self.db_connection.query_tempoCasa()
        for data in db_results:
            self._process_user(data)

    def _process_user(self, data):
        data_adm = self._parse_date(data.DATADM).strftime("%d/%m/%Y")
        aniversario_empresa = self._parse_date(data.DATADM).strftime("%d/%m")
        data_dem = self._parse_date(data.DATAFA).strftime("%d/%m/%Y") if data.DATAFA != datetime(1900, 12, 31) else datetime.now().strftime("%d/%m/%Y")
        cpf = data.NUMCPF
        
        self.hoje = datetime.now().strftime("%d/%m")
        if cpf not in self.data:
            self.data[cpf] = {
                'nome': data.NOMFUN,
                'situacao': data.SITAFA,
                'matriculas': [],
                'data_admissao':data_adm,
                'data_demissao':data_dem,
                'aniversario_empresa': aniversario_empresa,
                'email_pessoal': data.EMAPAR,
                'email_corporativo': data.EMACOM,
                'admissoes': []
            }

        self.data[cpf]['matriculas'].append((data_adm, data_dem))
        teste = self.data[cpf]['admissoes'].append((data_adm, data_dem))

        if data.SITAFA == 1:
            self._check_anniversary(cpf, data.NOMFUN, data_adm,aniversario_empresa)

    def _check_anniversary(self, cpf, nome, data_adm,aniversario_empresa):
        admissoes = self.data[cpf]['admissoes']
        tempo_de_casa = self.calcular_tempo_de_casa(admissoes)
        data_atual = datetime.now()
        primeiro_dia_proximo_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
        ultimo_dia_mes_atual = primeiro_dia_proximo_mes - timedelta(days=1)
        ultimodia = int(ultimo_dia_mes_atual.strftime('%d'))
        anos = tempo_de_casa.days // 365
        meses = (tempo_de_casa.days % 365) // ultimodia  # Assuming an average month length of 30 days
        admissoes.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
        data_admissao_antiga = None
        data_demissao_antiga = None
        if len(admissoes) > 1:
            data_admissao_antiga = datetime.strptime(admissoes[-2][0], "%d/%m/%Y").strftime("%d/%m/%Y")
            data_demissao_antiga = datetime.strptime(admissoes[-2][1], "%d/%m/%Y").strftime("%d/%m/%Y")
        # if anos in (5,10,15,20,25,30):
        if anos > 1 and aniversario_empresa == self.hoje:
            print(f"Aniversário de empresa de {nome.upper()} de {anos} {'anos' if anos > 1 else 'ano'} e {meses} {'meses' if meses > 1 else 'mês'} | Data de Admissão: {data_adm}{' Data de Admissão Antiga: ' + data_admissao_antiga  if data_admissao_antiga  else ''}{' Data de Demissao Antiga: ' + data_demissao_antiga  if data_demissao_antiga  else ''}")
            self._apply_filters(anos, self.data[cpf])

    def _apply_filters(self, anos, info):
        funcoes = {key: self._send_mail_star for key in (5, 10, 15, 20, 25, 30)}

        funcao = funcoes.get(anos, self.filtrar_aniversariantes)
        funcao(info, anos)
    def calcular_tempo_de_casa(self, admissoes):
        admissoes.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
        if len(admissoes) > 1:
            data_demissao_antiga = datetime.strptime(admissoes[-2][1], "%d/%m/%Y")
            data_admissao_nova = datetime.strptime(admissoes[-1][0], "%d/%m/%Y")
            diferenca_tempo = data_admissao_nova - data_demissao_antiga

            if diferenca_tempo < timedelta(days=180):
                data_admissao_antiga = datetime.strptime(admissoes[-2][0], "%d/%m/%Y")
                if data_admissao_antiga > datetime.now():
                    return timedelta(0)
                return datetime.now() - data_admissao_antiga
            else:
                if data_admissao_nova > datetime.now():
                    return timedelta(0)
                return datetime.now() - data_admissao_nova 
        else:
            data_admissao = datetime.strptime(admissoes[0][0], "%d/%m/%Y")
            if data_admissao > datetime.now():
                return timedelta(0)
            return datetime.now() - data_admissao
    def _parse_date(self, date_str):
        return date_str if isinstance(date_str, datetime) else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def filtrar_aniversariantes(self, info, anos):
        print(f"Filtrando aniversariantes para {anos} anos")  # Adicione esta linha
        self._send_mail_year(info, anos)

    def _send_mail_year(self, info, anos):
        if self.hoje == info['aniversario_empresa']:
            email = ["jhonny.souza@fgmdentalgroup.com"]  # ---------------------QAS-----------------------------
            # email = [f"{info['email_pessoal']}",f"{info['email_corporativo']}"]  # ---------------------PRD-----------------------------
            subject = f"Parabéns pelos {anos} anos de Casa {info['nome'].title()}!"
            body = self._generate_year_body( f'https://fgmdentalgroup.com/wp-content/uploads/2025/02/{anos}-anos.jpg','ImageBirth', f'https://fgmdentalgroup.com/Endomarketing/Tempo%20de%20casa/{anos}%20anos/index.html') #-----
            logging.info(f"Aniversáriantes da Empresa de {info['nome'].title()} Enviada para {email}")
            self._send_email(email, subject, body)
        else:
            logging.info(f"Nenhum aniversárianteno: {self.hoje}")
    def _send_mail_star(self, info, anos):
        if self.hoje == info['aniversario_empresa']:
            email = ["jhonny.souza@fgmdentalgroup.com"]  # ---------------------QAS-----------------------------
            # email = [f"{info['email_pessoal']}",f"{info['email_corporativo']}"]  # ---------------------PRD-----------------------------
            subject = f"Parabéns pelos {anos} anos de Casa {info['nome'].title()}!"
            body = self._generate_year_body(f'https://fgmdentalgroup.com/wp-content/uploads/2025/02/{anos}-anos-estrela.jpg', 'ImageBirth', f'https://fgmdentalgroup.com/Endomarketing/Tempo%20de%20casa/{anos}%20anos/index.html')
            print(f"Aniversáriantes da Empresa de {info['nome'].title()} Enviada para {email}, {info['nome']}")
            self._send_email(email, subject, body)
        else:
            logging.info(f"Nenhum aniversárianteno: {self.hoje}")
    def _generate_year_body(self,image_src, alt_text, link=None):
        if link:
            return f"""<html><br><body style="display: flex; justify-content: center; align-items: center;height: auto; margin: 0;">
                        <a href="{link}" style="display: flex; justify-content: center; align-items: center;">
                            <img src="{image_src}" alt="{alt_text}">
                        </a></body></html>"""
        else:
            return f"""<html><br><body style="display: flex; justify-content: center; align-items: center;height: auto; margin: 0;">
                        <a href="{link}" style="display: flex; justify-content: center; align-items: center;">
                            <img src="{image_src}" alt="{alt_text}">
                        </a></body></html>"""    

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
if __name__ == '__main__': 
    start = TempoCasa()
    start.connectionDB()