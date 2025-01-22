import oracledb
import logging
from collections import namedtuple
from config import host_data, port_data, service_name_data,user_data,password_data

class Database:
    def __init__(self):
        self.connection = None #Declara conexão como None
        self.cursor = None     #Declara cursor como None
    def connectData(self):
        dsn = {
            f'host': host_data,
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

    def query(self):
        if self.connection is None:
            logging.error("No database connection established.")
            return []
        row_data_list = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                SELECT
                    ROWNUM AS linha,
                    FUN.SITAFA AS SITAFA,
                    -- Situação
                    FUN.TIPADM AS TIPADM,
                    -- Tipo
                    FUN.NUMCAD AS NUMCAD,
                    -- Matrícula
                    FUN.DATADM AS DATADM,
                    -- Data Admissão
                    FUN.DATNAS AS DATNAS,
                    -- Data Nascimento
                    FUN.NOMFUN AS NOMFUN,
                    -- Nome completo
                    EM.EMAPAR AS EMAPAR,
                    -- Email pessoal
                    USU.NOMUSU AS NOMUSU,
                    -- Usuário 
                    FUN.CODCAR AS CODCAR,
                    -- Código cargo
                    CAR.TITCAR AS TITCAR,
                    -- Cargo
                    ORN.NOMLOC AS NOMLOC,
                    -- Setor
                    FUN.POSTRA AS POSTRA
                    -- Posto
                FROM
                    senior.R034FUN FUN
                INNER JOIN senior.R030EMP EMP ON
                    FUN.NUMEMP = EMP.NUMEMP
                INNER JOIN senior.R024CAR CAR ON
                    FUN.CODCAR = CAR.CODCAR
                    AND FUN.ESTCAR = CAR.ESTCAR
                INNER JOIN senior.R034CPL EM ON
                    FUN.NUMCAD = EM.NUMCAD
                INNER JOIN senior.R016ORN ORN ON
                    ORN.NUMLOC = FUN.NUMLOC
                INNER JOIN senior.R030FIL FIL ON
                    FUN.CODFIL = FIL.CODFIL
                    AND FUN.NUMEMP = FIL.NUMEMP
                LEFT JOIN senior.R034USU FUS ON
                    FUN.NUMEMP = FUS.NUMEMP
                    AND FUN.TIPCOL = FUS.TIPCOL
                    AND FUN.NUMCAD = FUS.NUMCAD
                LEFT JOIN senior.R999USU USU ON
                    FUS.CODUSU = USU.CODUSU
                LEFT JOIN senior.R034FOT PHO ON
                    FUN.NUMCAD = PHO.NUMCAD
                    AND FUN.TIPCOL = PHO.TIPCOL
                    AND FUN.NUMEMP = PHO.NUMEMP
                WHERE
                    FUN.SITAFA = '1'
                    AND FUN.TIPADM = '1'


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