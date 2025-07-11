# import os
# import logging
# from datetime import datetime
# from connectionDB import Database
# from sendMail import SendMail
# from tempoCasa import TempoCasa
# from getManager import Manager
# import socket
# class BithMail:
#     def __init__(self):
#         self.db = Database()
#         self.db.connectData()
#     @staticmethod
#     def logs():
#         nome_host = socket.gethostname()
#         ip_local = socket.gethostbyname(nome_host)
#         log_directory = r"/home/fgm/Scripts/BirthMail/Logs" #path para ser colocado as Logs
#         # diretorioLocal = os.getcwd()
#         # log_directory = f"{diretorioLocal}/Logs" #path para ser colocado as Logs
        
        
#         if not os.path.exists(log_directory):
#             os.makedirs(log_directory) #caso o path nao exista ele vai criar

#         current_datetime = datetime.now() #data de hoje
#         log_filename = os.path.join(log_directory, current_datetime.strftime("%Y-%m-%d") + "_log.log") #declara o nome do arquivo log
#         logging.basicConfig(
#             level=logging.INFO,
#             format="%(asctime)s %(levelname)s %(message)s",
#             encoding='utf-8',
#             datefmt="%Y-%m-%d %H:%M:%S",
#             filename=log_filename
#         )
#         logging.info(f"--------------Informações do executor--------------")
#         logging.info(f"IPV4: {ip_local}")
#         logging.info(f"HOST: {nome_host}") 

#     logs()
    
# if __name__ == "__main__":
#     start = SendMail()
#     start.send_birthday_emails()
#     start = TempoCasa()
#     start.connectionDB()
#     manager = Manager()
#     manager.connectionDB()
#     manager.birthMonth()
    