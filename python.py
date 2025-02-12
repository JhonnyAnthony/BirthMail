import socket
import getpass
nome_host = socket.gethostname()
ip_local = socket.gethostbyname(nome_host)
user = getpass.getuser()

print(f"O endereço IPv4 desta máquina é: {ip_local} user {user}")