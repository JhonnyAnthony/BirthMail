import oracledb
import logging
from collections import namedtuple
from config import host_data, port_data, service_name_data, user_data, password_data

class Database:
    def __init__(self):
        self.connection = None  # Declara conexão como None
        self.cursor = None      # Declara cursor como None

    def connectData(self):
        dsn = {
            'host': host_data,
            'port': port_data,
            'service_name': service_name_data,
            'user': user_data,
            'password': password_data
        }

        # Check if environment variables are loaded
        if None in dsn.values():
            logging.error("Missing one or more environment variables.")
            return
        try:
            self.connection = oracledb.connect(
                user=dsn['user'],
                password=dsn['password'],
                dsn=oracledb.makedsn(dsn['host'], dsn['port'], service_name=dsn['service_name'])
            )
            logging.info("Database connection established successfully.")
        except oracledb.DatabaseError as e:
            logging.error("Error establishing connection: %s", e)

    def executeQuery(self, query):
        if self.connection is None:
            logging.error("No database connection established.")
            return []
        row_data_list = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute(query)
            RowData = namedtuple('RowData', [desc[0] for desc in self.cursor.description])
            rows = self.cursor.fetchall()
            for row in rows:
                row_data_object = RowData(*row)
                row_data_list.append(row_data_object)
            logging.info("Query executed successfully.")
        except oracledb.DatabaseError as e:
            logging.error("Error executing query: %s", e)
        finally:
            if self.cursor:
                self.cursor.close()
        return row_data_list

    def closeConnection(self):
        if self.connection:
            self.connection.close()
            logging.info("Database connection closed.")