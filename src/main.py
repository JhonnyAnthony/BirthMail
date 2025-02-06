import os
import logging
from datetime import datetime
from connectionDB import Database
from sendMail import SendMail
from getManager import Manager
class BithMail:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def logs():
        #log_directory = r"/home/fgm/Scripts/BirthMail/Logs" #path para ser colocado as Logs
        diretorioLocal = os.getcwd()
        log_directory = f"{diretorioLocal}/Logs" #path para ser colocado as Logs

        if not os.path.exists(log_directory):
            os.makedirs(log_directory) #caso o path nao exista ele vai criar

        current_datetime = datetime.now() #data de hoje
        log_filename = os.path.join(log_directory, current_datetime.strftime("%Y-%m-%d") + "_log.log") #declara o nome do arquivo log

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_filename
        )
    logs()
    
if __name__ == "__main__":
    start = SendMail()
    start.send_birthday_emails()
    manager = Manager()
    manager.connectionDB()
    manager.birthMonth()