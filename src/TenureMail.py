from dateutil.relativedelta import relativedelta
from connectionDB import Database
from datetime import datetime, timedelta
from config import client_secret, client_id, tenant_id, scope, email_from
import locale
import requests
import logging
import json

class TenureMail:
    # Cria um "objeto"
    def __init__(self):
        self.db_connection = Database()
        self.db_connection.connectData()
        self.data = {}
        self.supervisores = {}
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    # Conexção com Banco de Dados
    def ConnectionDB(self):
        try:
            db_results = self.db_connection.query_tempoCasa()
            lista_aniversario = []
            for data in db_results:
                self.processa_usuario(data, lista_aniversario)
            nome_mes_seguinte = self.mes_seguinte.strftime("%B").title()
            self.enviar_lista_mail(lista_aniversario,nome_mes_seguinte)
        except Exception as e:
            logging.error("Error processing database results: %s", e)

    # Processamento de usuario 
    def processa_usuario(self, data,lista_aniversario):
       
        self.emailToday = ["gestaodepessoas@fgmdentalgroup.com", "grupo.coordenadores@fgmdentalgroup.com", "grupo.supervisores@fgmdentalgroup.com", "grupo.gerentes@fgmdentalgroup.com"]  # Email aniversário diário PRD
        # self.emailToday = ["sophia.alberton@fgmdentalgroup.com"]  # QAS Email aniversário diário        
        data_adm = self.parse_date(data.DATADM).strftime("%d/%m/%Y")
        aniversario_empresa = self.parse_date(data.DATADM).strftime("%d/%m")
        mes_aniversario = self.parse_date(data.DATADM).strftime("%m")
        data_dem = self.parse_date(data.DATAFA).strftime("%d/%m/%Y") 
        cpf = data.NUMCPF        
        self.mes_seguinte = datetime.now() + relativedelta(months=1)
        self.hoje = datetime.now().strftime("%d/%m")
        self.data_fixa = datetime.now().strftime("%d")
        if cpf not in self.data:
            self.data[cpf] = {
                'nome': data.NOMFUN,
                'situacao': data.SITAFA,
                'matriculas': [],
                'data_admissao':data_adm,
                'data_demissao':data_dem,
                'aniversario_empresa': aniversario_empresa,
                'mes_aniversario': mes_aniversario,
                'email_pessoal': data.EMAPAR,
                'email_corporativo': data.EMACOM,
                'admissoes': []
            }
        self.data[cpf]['matriculas'].append((data_adm, data_dem))
        self.data[cpf]['admissoes'].append((data_adm, data_dem))

        if data.SITAFA != 7:
            self.check_aniversario(cpf, data.NOMFUN,aniversario_empresa,mes_aniversario,lista_aniversario)

    # Calcula o tempo de casa do funcionario
    def calcular_tenure(self, admissoes):
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
        
    # Caclula aniversario de casa do funcionario
    def check_aniversario(self, cpf, nome,aniversario_empresa,mes_aniversario,lista_aniversario):
        admissoes = self.data[cpf]['admissoes']
        tempo_de_casa = self.calcular_tenure(admissoes)
        data_atual = datetime.now()
        primeiro_dia_proximo_mes = (data_atual.replace(day=28) + timedelta(days=4)).replace(day=1)
        ultimo_dia_mes_atual = primeiro_dia_proximo_mes - timedelta(days=1)
        ultimodia = int(ultimo_dia_mes_atual.strftime('%d'))
        anos = tempo_de_casa.days // 365
        admissoes.sort(key=lambda x: datetime.strptime(x[0], "%d/%m/%Y"))
        data_admissao_antiga = None
        data_demissao_antiga = None
        lista_ignorados = []
        self.mes_seguinte.strftime("%B").title()

        mes_seguintes = self.mes_seguinte.strftime("%m") 
        if len(admissoes) > 1:
            data_admissao_antiga = datetime.strptime(admissoes[-2][0], "%d/%m/%Y")
            data_admissao_nova = datetime.strptime(admissoes[-1][0], "%d/%m/%Y")
            data_demissao_antiga = datetime.strptime(admissoes[-2][1], "%d/%m/%Y")
            diferenca_tempo = (data_admissao_nova - data_demissao_antiga)
            if diferenca_tempo < timedelta(days=180) or nome == ('RODRIGO DE OLIVEIRA LUIZ'):
                data_admissao_antiga.strftime("%d/%m/%Y")
                data_admissao_nova.strftime("%d/%m/%Y")
                lista_ignorados.append((nome,aniversario_empresa))
        
        if anos >= 1 and mes_seguintes == mes_aniversario and (nome, aniversario_empresa) not in lista_ignorados:
            # Esse log vai listar aniversariantes de tempo de empresa
            lista_aniversario.append((nome,aniversario_empresa,anos))
     
    # Formata data para poder calcular 
    def parse_date(self, date_str):
        return date_str if isinstance(date_str, datetime) else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Chama funções que envia email
    def enviar_lista_mail(self,lista_aniversario,nome_mes_seguinte):
        dia_inicio = '28'
        if dia_inicio == self.data_fixa:
            logging.info("enviar_lista_mail -> Chama as funções que gera a lista e envia a lista")
            subject = f'Aniversariantes do mês de {nome_mes_seguinte}'
            email = self.emailToday # ---------------------------------
            body = self.gerador_lista_mail(lista_aniversario,nome_mes_seguinte) #-----
            self.enviar_mail(email, subject, body)
            
            logging.info(f"enviar_lista_mail -> Gerou email com lista e enviou para {email}")
            # self.filtrar_admitidos_no_proximo_mes(lista_aniversario, nome_mes_seguinte)
            
     # Gera corpo de email com lista                        
    def gerador_lista_mail(self, lista_aniversario,nome_mes_seguinte):
        logging.info("gerador_lista_mail -> Gerando lista e email")
        body = f"<strong>Bom dia,</strong><br>Segue a lista de colaboradores que fazem aniversário de empresa no mês de {nome_mes_seguinte}:<br><br>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += """
            <tr style="background-color: #d3d3d3; color: black;">
                <th>Colaboradores Aniversariantes</th>
                <th>Data</th>
                <th>Anos de Empresa</th>
            </tr>
        """      
        # print(lista_aniversariantes)
        for nome,data,anos in lista_aniversario:
            body += f"<tr><td>{nome}</td><td>{data}</td><td>{anos}</td></tr>"
        body += "</table><br>Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body
       
    # Prepara e envia email    
    def enviar_mail(self, email_to, subject, body):
        logging.info("enviar_mail -> Função que envia o email")
        email_group = email_to
        token = self.obter_acesso_token()
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
            logging.info(f"enviar_mail -> E-mail pronto para enviar para {email_group}")
            # logging.info("------------------------------------------------------------------------------------")            
        else:
            logging.error(f'enviar_mail -> Falha ao preparar envio de e-mail: {response.status_code}: {response.text}')

    # Acesso Token
    def obter_acesso_token(self):
        url = f'https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token'
        data = {
            'grant_type': 'client_credentials',
            'client_id': client_id,
            'client_secret': client_secret,
            'scope': scope
        }
        response = requests.post(url, data=data)
        return response.json().get('access_token')
