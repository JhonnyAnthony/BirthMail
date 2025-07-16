from dateutil.relativedelta import relativedelta
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
        self.supervisores = {}
        locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    def connectionDB(self):
        try:
            db_results = self.db_connection.query_tempoCasa()
            lista_aniversario = []
            for data in db_results:
                self._process_user(data, lista_aniversario)
            nome_mes_seguinte = self.mes_seguinte.strftime("%B").title()
            self.send_mail_list(lista_aniversario,nome_mes_seguinte)
        except Exception as e:
            logging.error("Error processing database results: %s", e)

    def _process_user(self, data,lista_aniversario):
        data_adm = self._parse_date(data.DATADM).strftime("%d/%m/%Y")
        aniversario_empresa = self._parse_date(data.DATADM).strftime("%d/%m")
        mes_aniversario = self._parse_date(data.DATADM).strftime("%m")
        # mes_aniversario = aniversario_empresa.strftime("%m")
        data_dem = self._parse_date(data.DATAFA).strftime("%d/%m/%Y") 
        # estpos = data.ESTPOS
        # postra = data.POSTRA
        # email_supervisor = [self.db_connection.query_mailsup(estpos, postra)]
        # self.nome_supervisor = self.db_connection.query_nomesup(estpos, postra)
        # self.emailToday = ["gestaodepessoas@fgmdentalgroup.com", "grupo.coordenadores@fgmdentalgroup.com", "grupo.supervisores@fgmdentalgroup.com", "grupo.gerentes@fgmdentalgroup.com"]  # Email aniversário diário
        self.emailToday = ["sophia.alberton@fgmdentalgroup.com", "jhonny.souza@fgmdentalgroup.com"]  # Email aniversário diário

        # if data.DATAFA != datetime(1900, 12, 31) else datetime.now().strftime("%d/%m/%Y")
        cpf = data.NUMCPF        
        self.mes_seguinte = datetime.now() + relativedelta(months=1)
        self.hoje = datetime.now().strftime("%d/%m")
        
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
        teste = self.data[cpf]['admissoes'].append((data_adm, data_dem))

        if data.SITAFA != 7:
            self._check_anniversary(cpf, data.NOMFUN, data_adm,aniversario_empresa,mes_aniversario,lista_aniversario)

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
        
    def _check_anniversary(self, cpf, nome, data_adm,aniversario_empresa,mes_aniversario,lista_aniversario):
        admissoes = self.data[cpf]['admissoes']
        # print(nome,admissoes)
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
        lista_ignorados = []
        nome_mes_seguinte = self.mes_seguinte.strftime("%B").title()

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
                # print(f"LISTA {lista_ignorados}")
        if aniversario_empresa == self.hoje and (nome,aniversario_empresa) in lista_ignorados:
            logging.info("Enviada lista de Duplicados")
            self._send_mail_rh(nome,aniversario_empresa)
        # if anos > 1 and aniversario_empresa == self.hoje and (nome,aniversario_empresa) not in lista_ignorados:
        #     logging.info(f"Aniversário de empresa de {nome.upper()} de {anos} {'anos' if anos > 1 else 'ano'} e {meses} {'meses' if meses > 1 else 'mês'} ")
        #     self._apply_filters(anos, self.data[cpf])
        if anos > 1 and mes_seguintes == mes_aniversario and (nome, aniversario_empresa) not in lista_ignorados:
            # logging.info(f"Lista de aniversáriantes de tempo de empresa {nome.upper()} de {anos} {'anos' if anos > 1 else 'ano'} e {meses} {'meses' if meses > 1 else 'mês'} ")
            lista_aniversario.append((nome,aniversario_empresa,anos))
            # self.send_mail_list(lista_aniversario,nome_mes_seguinte)
                        
    def _apply_filters(self, anos, mes_seguintes, info):
        funcoes = {key: self._send_mail_star for key in (5, 10, 15, 20, 25, 30)}
        
        funcao = funcoes.get(anos, self.filtrar_aniversariantes)
        funcao(info, anos)                
     
    def _parse_date(self, date_str):
        return date_str if isinstance(date_str, datetime) else datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    def filtrar_aniversariantes(self, info, anos):
        print(f"Filtrando aniversariantes de {anos} anos")  # Adicione esta linha
        
        self._send_mail_year(info, anos)  
    
    def send_mail_list(self,lista_aniversario,nome_mes_seguinte):
            subject = f'Aniversariantes do mês de {nome_mes_seguinte}'
            email = self.emailToday # ---------------------QAS-----------------------------
            body = self._generate_list_mail(lista_aniversario,nome_mes_seguinte) #-----
            logging.info(f"Lista enviada para {email}")
            self._send_email(email, subject, body)
            # self.filtrar_admitidos_no_proximo_mes(lista_aniversario, nome_mes_seguinte)
                                
    def _generate_list_mail(self, lista_aniversario,nome_mes_seguinte):
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
    
    def _send_mail_rh(self,nome,aniversario_empresa):
            # email = [f"vanessa.boing@fgmdentalgroup.com"]  # ---------------------PRD-----------------------------
            email = ["sophia.alberton@fgmdentalgroup.com","jhonny.souza@fgmdentalgroup.com"] # ---------------------QAS-----------------------------
            subject = f"Lista de aniversáriantes com duas matriculas"
            body = self._generate_rh_mail(nome,aniversario_empresa) #-----
            logging.info(f"Lista enviada para {email}")
            self._send_email(email, subject, body)
    
    #enviando email para o aniversariante
    def _send_mail_year(self, info, anos):
        if self.hoje == info['aniversario_empresa']:
            # email = [f"{info['email_pessoal']}",f"{info['email_corporativo']}"]  # ---------------------PRD-----------------------------
            email = ["sophia.alberton@fgmdentalgroup.com","jhonny.souza@fgmdentalgroup.com"] # ---------------------QAS-----------------------------
            subject = f"Parabéns pelos {anos} anos de FGM - {info['nome'].title()}!"
            body = self._generate_year_body( f'https://fgmdentalgroup.com/wp-content/uploads/2025/02/{anos}-anos.jpg','ImageBirth','https://fgmdentalgroup.com/Endomarketing/Tempo%20de%20casa/Geral/index.html') #-----
            logging.info(f"Aniversáriantes da Empresa de {info['nome'].title()} Enviada para {email}")
            self._send_email(email, subject, body)
        else:
            logging.info(f"Nenhum aniversárianteno: {self.hoje}")
        
    def _send_mail_star(self, info, anos):
        if self.hoje == info['aniversario_empresa']:
            # email = [f"{info['email_pessoal']}",f"{info['email_corporativo']}"]  # ---------------------PRD-----------------------------
            email = ["sophia.alberton@fgmdentalgroup.com","jhonny.souza@fgmdentalgroup.com"] # ---------------------QAS-----------------------------
            subject = f"Parabéns pelos {anos} anos de FGM - {info['nome'].title()}!"
            body = self._generate_year_body(f'https://fgmdentalgroup.com/wp-content/uploads/2025/02/{anos}-anos-estrela.jpg', 'ImageBirth', f'https://fgmdentalgroup.com/Endomarketing/Tempo%20de%20casa/{anos}%20anos/index.html')
            print(f"Aniversáriantes da Empresa de {info['nome'].title()} Enviada para {email}, {info['nome']}")
            # self._send_email(email, subject, body)
        else:
            logging.info(f"Nenhum aniversárianteno: {self.hoje}")
        
    def _send_birthday_today_mail(self, aniversariantes, data_aniversario,ano):
        if  '29/02' in data_aniversario and ano != 'bissexto' and self.hoje == '27/02':
            # email_morning = self.emailToday       #---------------------PRD-----------------------------
            email_morning = self.email_teste    #---------------------QAS-----------------------------
            subject = f'Aniversariantes do dia'
            body = self._generate_dayling_email_body(aniversariantes,ano)
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info(f'Lista de Aniversáriantes do dia Enviada')
            self._send_email(email_morning, subject, body)
        elif  self.hoje in data_aniversario :
            # email_morning = self.emailToday       #---------------------PRD-----------------------------
            email_morning = self.email_teste    #---------------------QAS-----------------------------
            subject = f'Aniversariantes do dia'
            body = self._generate_dayling_email_body(aniversariantes,ano)
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info(f'Lista de Aniversáriantes do dia Enviada')
            print("Email Aniversário Diário")
            self._send_email(email_morning, subject, body)
        else: 
            logging.info(f"--------------Informações do Envio de Email--------------")
            logging.info("Sem aniversáriantes no dia!") 
        
    def _send_birth_superior_mail(self, aniversariantes_mes): 
        count = 0
        hoje = datetime.now().strftime("%d/%m")
        mesStart = datetime.now().month
        diaFixo = 27 
        data_fixa = datetime(datetime.now().year, mesStart, diaFixo)
        diaStart = (data_fixa.strftime("%d/%m"))
        if hoje == diaStart:
            for supervisor, info in aniversariantes_mes.items(): 
                count += 1
                # emailSupervisor = info["email"]       #---------------------PRD-----------------------------
                emailSupervisor = self.email_teste    #---------------------QAS-----------------------------
                funcionarios = info["funcionarios"]     
                mes_seguinte = datetime.now() + relativedelta(months=1)
                mes_seguinte = mes_seguinte.strftime("%B").title()
                subject = f'Aniversariantes do mês de {mes_seguinte}' # Define o assunto do e-mail 
                body = self._generate_supervisor_email_body(supervisor, funcionarios,mes_seguinte) # Gera o corpo do e-mail 
                logging.info(f'Lista de Aniversáriantes de {supervisor} do mes de {mes_seguinte}')
                print(f"Contagem: {count}")
                self._send_email(emailSupervisor, subject, body) # Envia o e-mail    
            
    # listagem mensal dos colaboradores que fazem aniversario de tempo de casa
    def _send_list_mounth(self):
        # aniversariantes = self.filtrar_aniversariantes_do_mes()
        # aniversariantes_mes = self.filtrar_aniversariantes_do_mes_seguinte()
        aniversariantes = self.filtrar_admitidos_do_dia()
        aniversariantes_mes = self.filtrar_admitidos_no_proximo_mes()
        data_aniversario = self.filtrar_datas(aniversariantes)
        ano = datetime.now().year
        if ano % 4 == 0: ano = 'bissexto' #Verifica se o ano é bissexto

        if aniversariantes:
            self._send_birthday_today_mail(aniversariantes, data_aniversario,ano)                  
            self._send_mail_rh(aniversariantes_mes)
            self._send_birth_superior_mail(aniversariantes_mes) 
    
    def _generate_dayling_email_body(self, aniversariantes,ano):
        body = f"<strong>Olá Liderança. Segue a lista de colaboradores que fazem aniversário de tempo de casa este mês:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += """<tr style="background-color: #d3d3d3; color: black;"><th>Colaboradores Aniversáriantes</th><th>Data</th><th>Setor</th></tr>""" 

        # Colete todos os aniversariantes em uma única lista
        todos_aniversariantes = []
        for supervisor, info in aniversariantes.items():
            for funcionario, data_admissao, local in info["funcionarios"]:
                if self.hoje in data_admissao:
                    todos_aniversariantes.append((funcionario, data_admissao, local))
                elif data_admissao == '29/02' and ano != 'bissexto' and self.hoje == '27/02' : #FILTRO DE ANIVERSÁRIO DIA 29/02 SEM ANO BISSEXTO
                    todos_aniversariantes.append((funcionario, data_admissao, local))
        # Ordene todos os aniversariantes por nome do colaborador
        todos_aniversariantes.sort(key=lambda x: x[0])

        # Construa a tabela
        for funcionario, data_admissao, local in todos_aniversariantes:
            body += f"<tr><td>🎂{funcionario}</td><td>📅{data_admissao}</td><td>{local}</td></tr>"

        body += "</table><br>"
        body += "Atenciosamente,<br>Equipe de Gestão de Pessoas"
        return body

    def _generate_rh_mail(self,nome,aniversario_empresa):
        body = f"<strong>Olá Vanessa. Segue a lista de colaboradores que fazem aniversário hoje que tem duas matriculas:<br><br></strong>"
        body += "<table border='1' cellpadding='5' cellspacing='0'>"
        body += """<tr style="background-color: #d3d3d3; color: black;">
                    <th>Colaboradores Aniversáriantes</th><th>Data</th></tr>""" 

        body += f"""<tr><td>{nome}</td><td>{aniversario_empresa}</td></tr><br>"""
        return body

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
