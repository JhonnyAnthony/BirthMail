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
            logging.info(f"--------------Informações da Database--------------")
            logging.info("Database connection established successfully.")
            

        except oracledb.DatabaseError as e:
            logging.error("Error establishing connection: %s", e)

    def query_principal(self):
        if self.connection is None:
            logging.error("No database connection established.")
            return []
        row_data_list = []
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                SELECT *
                FROM(
                SELECT
                    FUN.SITAFA AS SITAFA, -- Situação
                    FUN.NUMCAD AS NUMCAD, -- Matrícula
                    FUN.DATADM AS DATADM, -- Data Admissão
                    FUN.DATNAS AS DATNAS, -- Data Nascimento
                    FUN.NOMFUN AS NOMFUN, -- Nome completo
                    EM.EMAPAR AS EMAPAR, -- Email pessoal
                    USU.NOMUSU AS NOMUSU, -- Usuário
                    FUN.CODCAR AS CODCAR, -- Código cargo
                    CAR.TITCAR AS TITCAR, -- Cargo
                    ORN.NOMLOC AS NOMLOCAL, -- Setor
                    FUN.NUMLOC AS NUMLOC, -- Local
                    FUN.POSTRA,
                    SUP.NOMFUN AS NOMESUP, -- Nome do supervisor
                    ROW_NUMBER() OVER (PARTITION BY FUN.NUMCAD ORDER BY FUN.NUMCAD) AS RN
            
                FROM
                    senior.R034FUN FUN
                INNER JOIN senior.R030EMP EMP ON FUN.NUMEMP = EMP.NUMEMP
                INNER JOIN senior.R024CAR CAR ON FUN.CODCAR = CAR.CODCAR AND FUN.ESTCAR = CAR.ESTCAR
                LEFT JOIN senior.R034CPL EM ON FUN.NUMCAD = EM.NUMCAD
                INNER JOIN senior.R016ORN ORN ON ORN.NUMLOC = FUN.NUMLOC
                INNER JOIN senior.R030FIL FIL ON FUN.CODFIL = FIL.CODFIL AND FUN.NUMEMP = FIL.NUMEMP
                LEFT JOIN senior.R034USU FUS ON FUN.NUMEMP = FUS.NUMEMP AND FUN.TIPCOL = FUS.TIPCOL AND FUN.NUMCAD = FUS.NUMCAD
                LEFT JOIN senior.R999USU USU ON FUS.CODUSU = USU.CODUSU
                LEFT JOIN senior.R034FOT PHO ON FUN.NUMCAD = PHO.NUMCAD AND FUN.TIPCOL = PHO.TIPCOL AND FUN.NUMEMP = PHO.NUMEMP
                LEFT JOIN senior.R034FUN SUP ON FUN.POSTRA = SUP.POSTRA AND SUP.SITAFA <> 7
                WHERE
                    FUN.SITAFA != 7
                    AND FUN.TIPCOL = '1'
                    AND CAR.TITCAR != 'PENSIONISTA')
                WHERE RN  IN (1,2,3,4,5,6)
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
            logging.info("Cursor closed.")
        return row_data_list
        
    

    def query_idepos(self, ESTPOS, POSTRA):
        if self.connection is None:
            logging.error("No database connection established.")
            return None
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                SELECT Z.IDEPOS
                FROM senior.R017HIE Z
                WHERE Z.ESTPOS = :estpos
                AND ROWNUM <= 1
                AND Z.POSPOS = (
                    SELECT SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                    FROM senior.R017HIE HIE
                    WHERE HIE.ESTPOS = :estpos
                    AND HIE.POSTRA = :postra
                    AND ROWNUM <= 1
                ) AS IDEPOS,
            """, estpos=ESTPOS, postra=POSTRA)
            row = self.cursor.fetchone()
            logging.info("Query executed successfully.")
            return row[0] if row else None
        except oracledb.DatabaseError as e:
            logging.error("Error executing query: %s", e)
        finally:
            if self.cursor:
                self.cursor.close()
            logging.info("Cursor closed.")

    def query_nomesup(self, ESTPOS, POSTRA):
        if self.connection is None:
            logging.error("No database connection established.")
            return None
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                SELECT K.NOMFUN
                FROM senior.R034FUN K
                WHERE ROWNUM = 1
                AND K.SITAFA <> 7
                AND K.ESTPOS = :estpos
                AND K.POSTRA = (
                    SELECT Z.POSTRA
                    FROM senior.R017HIE Z
                    WHERE Z.ESTPOS = :estpos
                    AND ROWNUM <= 1
                    AND Z.POSPOS = (
                        SELECT SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                        FROM senior.R017HIE HIE
                        WHERE HIE.ESTPOS = :estpos
                        AND HIE.POSTRA = :postra
                        AND ROWNUM <= 1
                    )
                ) AS NOMESUP,
            """, estpos=ESTPOS, postra=POSTRA)
            row = self.cursor.fetchone()
            logging.info("Query executed successfully.")
            return row[0] if row else None
        except oracledb.DatabaseError as e:
            logging.error("Error executing query: %s", e)
        finally:
            if self.cursor:
                self.cursor.close()
            logging.info("Cursor closed.")

    def query_usersup(self, ESTPOS, POSTRA):
        if self.connection is None:
            logging.error("No database connection established.")
            return None
        try:
            self.cursor = self.connection.cursor()
            self.cursor.execute("""
                SELECT SUP.NOMUSU
                FROM senior.R034FUN K
                INNER JOIN senior.R034USU F ON K.NUMEMP = F.NUMEMP AND K.TIPCOL = F.TIPCOL AND K.NUMCAD = F.NUMCAD
                INNER JOIN senior.R999USU SUP ON F.CODUSU = SUP.CODUSU
                WHERE ROWNUM = 1
                AND K.SITAFA <> 7
                AND K.ESTPOS = :estpos
                AND K.POSTRA = (
                    SELECT Z.POSTRA
                    FROM senior.R017HIE Z
                    WHERE Z.ESTPOS = :estpos
                    AND ROWNUM <= 1
                    AND Z.POSPOS = (
                        SELECT SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                        FROM senior.R017HIE HIE
                        WHERE HIE.ESTPOS = :estpos
                        AND HIE.POSTRA = :postra
                        AND ROWNUM <= 1
                    )
                )
            """, estpos=ESTPOS, postra=POSTRA)
            row = self.cursor.fetchone()
            logging.info("Query executed successfully.")
            return row[0] if row else None
        except oracledb.DatabaseError as e:
            logging.error("Error executing query: %s", e)
        finally:
            if self.cursor:
                self.cursor.close()
            logging.info("Cursor closed.")

    