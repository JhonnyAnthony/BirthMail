import sys
sys.path.append('C:/Github/BirthMail/src')
from connectionDB import Database

class Connection:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def connection(self):
        return self.db.query()
