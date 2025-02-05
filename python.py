from datetime import datetime

mesStart = datetime.now().month
diaStart = 28
data_fixa = datetime(datetime.now().year, mesStart, diaStart)
teste = (data_fixa.strftime("%d/%m"))
print(teste)