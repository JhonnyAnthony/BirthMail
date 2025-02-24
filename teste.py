from datetime import datetime

# Obter o ano atual
ano_atual = datetime.now().year

# Verificar se o ano é bissexto
if (ano_atual % 4 == 0 and ano_atual % 100 != 0) or (ano_atual % 400 == 0):
    dias_no_ano = 366
else:
    dias_no_ano = 365

print(f"O ano de {ano_atual} tem {dias_no_ano} dias.")