import oracledb
import os
import logging
from dotenv import load_dotenv
from collections import namedtuple


# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '..', 'venv', '.env')
load_dotenv(dotenv_path)

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None

    def connectData(self):
        dsn = {
            'host': os.getenv('host'),
            'port': os.getenv('port'),
            'service_name': os.getenv('service_name'),
            'user': os.getenv('user'),
            'password': os.getenv('password')
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

    def query(self):
        if self.connection is None:
            logging.error("No database connection established.")
            return []

        row_data_list = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                SELECT
                    R034FUN.NUMEMP AS NUMEMP,
                    R034FUN.TIPCOL AS TIPCOL,
                    R034FUN.NUMCAD AS NUMCAD,
                    R034FUN.NOMFUN AS NOMFUN,
                    R034FUN.TIPADM AS TIPADM,
                    R034FUN.SITAFA AS SITAFA,
                    R034FUN.DATNAS AS DATNAS,
                    R999USU.CODUSU AS CODUSU,
                    R999USU.NOMUSU AS NOMUSU,
                    R034CPL.EMAPAR AS EMAPAR
                FROM
                    SENIOR.R034FUN
                INNER JOIN
                    SENIOR.R034USU
                ON
                    R034FUN.NUMCAD = R034USU.NUMCAD
                INNER JOIN
                    SENIOR.R999USU
                ON
                    R034USU.CODUSU = R999USU.CODUSU
                INNER JOIN
                    SENIOR.R034CPL
                ON
                    R034FUN.NUMCAD = R034CPL.NUMCAD
                WHERE
                    R034FUN.SITAFA = '1'
                AND
                    R034FUN.TIPCOL = '1'
            """)
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
            if self.connection:
                self.connection.close()
            logging.info("Database connection closed.")
        return row_data_list