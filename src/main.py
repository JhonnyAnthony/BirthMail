import os
import json
import logging
import requests
from datetime import datetime

from config import client_secret, client_id, tenant_id, scope, email_from

class BithMail:
    def __init__(self):
        pass
    @staticmethod
    def logs():
        log_directory = r"C:/Github/BirthMail/Logs"
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)

        current_datetime = datetime.now()
        log_filename = os.path.join(log_directory, current_datetime.strftime("%Y-%m-%d") + "_log.log")

        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            filename=log_filename
        )
    logs()

if __name__ == "__main__": #Inicia o Projeto
    main = BithMail()