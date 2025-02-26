import requests
from PIL import Image, ImageDraw, ImageFont
from connectionDB import Database
from io import BytesIO
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecurePlatformWarning)

class NomeImagem:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def send_birthday_emails(self):
        resultados = self.db.query_principal()  # Armazena dados dos Usuários
        seen = set()  # Conjunto para rastrear nomes de usuários únicos
        for resultado in resultados:  # Loop para verificar todos os Usuários
            self._process_user(resultado, seen)

    def _process_user(self, resultado, seen):
        if resultado.NOMFUN not in seen:  # Verifica se o nome já foi processado
            seen.add(resultado.NOMFUN)
            self.nomeFun = resultado.NOMFUN  # Define o atributo nomeFun
            # Chamar o método que você deseja executar
            self.nomeUsuario = resultado.NOMUSU
            self.Imagem()

    def Imagem(self):
        url = "https://fgmdentalgroup.com/wp-content/uploads/2025/02/imagem.jpg"

        # Fazer o download da imagem
        response = requests.get(url, verify=False)
        imagem = Image.open(BytesIO(response.content))

        # Criação de um objeto de desenho
        draw = ImageDraw.Draw(imagem)

        # Definir a fonte (você pode usar uma fonte TTF que esteja disponível no seu sistema)
        fonte = ImageFont.truetype("arial.ttf", 55)

        # Texto a ser adicionado
        texto = self.nomeFun

        # Obter largura e altura da imagem
        largura_img, altura_img = imagem.size

        # Função para quebrar o texto em várias linhas
        def quebra_texto(texto, largura_maxima, draw, fonte):
            palavras = texto.split()
            linhas = []
            linha_atual = ""
            for palavra in palavras:
                linha_imagem = linha_atual + " " + palavra if linha_atual else palavra
                bbox = draw.textbbox((0, 0), linha_imagem, font=fonte)
                largura_imagem = bbox[2] - bbox[0]
                if largura_imagem <= largura_maxima:
                    linha_atual = linha_imagem
                else:
                    linhas.append(linha_atual)
                    linha_atual = palavra
            if linha_atual:
                linhas.append(linha_atual)
            return linhas

        # Quebrar o texto em várias linhas, se necessário
        linhas = quebra_texto(texto, largura_img - 40, draw, fonte)  # largura_img - 40 para margem

        # Fixar a posição vertical do texto
        posicao_y_fixa = 160  # Defina aqui a posição vertical fixa

        # Cor do texto (R, G, B)
        cor_do_texto = (255, 255, 255)

        # Adicionar cada linha de texto à imagem
        for i, linha in enumerate(linhas):
            bbox = draw.textbbox((0, 0), linha, font=fonte)
            largura_texto, altura_texto = bbox[2] - bbox[0], bbox[3] - bbox[1]
            posicao_x = (largura_img - largura_texto) / 2
            posicao_y = posicao_y_fixa + i * (altura_texto + 5)  # 5 é o espaçamento entre as linhas
            draw.text((posicao_x, posicao_y), linha, font=fonte, fill=cor_do_texto)

        # Salvar a imagem modificada
        imagemModificada = imagem.save("src/imagem_modificada.png")

        print("Texto adicionado à imagem com sucesso!")

# Exemplo de uso
nome_imagem = NomeImagem()
resultados = nome_imagem.db.query_principal()  # Assume-se que a consulta já está correta
for resultado in resultados:
    nome_imagem._process_user(resultado, set())
