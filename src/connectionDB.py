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
                    FUN.POSTRA,
                    (
                    SELECT
                        Z.POSTRA
                    FROM
                        senior.R017HIE Z
                    WHERE
                        Z.ESTPOS = FUN.ESTPOS
                        AND ROWNUM <= 1
                        AND Z.POSPOS = (
                        SELECT
                            SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                        FROM
                            senior.R017HIE HIE
                        WHERE
                            HIE.ESTPOS = FUN.ESTPOS
                            AND HIE.POSTRA = FUN.POSTRA
                            AND ROWNUM <= 1
                        )
                    ) AS POSTRA_CHE,
                    (
                    SELECT
                        K.NOMFUN
                    FROM
                        senior.R034FUN K
                    WHERE
                        ROWNUM = 1
                        AND K.SITAFA <> 7
                        AND K.ESTPOS = FUN.ESTPOS
                        AND K.POSTRA = (
                        SELECT
                            Z.POSTRA
                        FROM
                            senior.R017HIE Z
                        WHERE
                            Z.ESTPOS = FUN.ESTPOS
                            AND ROWNUM <= 1
                            AND Z.POSPOS = (
                            SELECT
                                SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                            FROM
                                senior.R017HIE HIE
                            WHERE
                                HIE.ESTPOS = FUN.ESTPOS
                                AND HIE.POSTRA = FUN.POSTRA
                                AND ROWNUM <= 1
                            )
                        )
                    ) AS NOMESUP,
                    (
                    SELECT
                        SUP.NOMUSU
                    FROM
                        senior.R034FUN K
                    INNER JOIN senior.R034USU F ON
                        K.NUMEMP = F.NUMEMP
                        AND K.TIPCOL = F.TIPCOL
                        AND K.NUMCAD = F.NUMCAD
                    INNER JOIN senior.R999USU SUP ON
                        F.CODUSU = SUP.CODUSU
                    INNER JOIN senior.R034FOT PHO ON
                        K.NUMCAD = PHO.NUMCAD
                        AND K.TIPCOL = PHO.TIPCOL
                        AND K.NUMEMP = PHO.NUMEMP
                    WHERE
                        ROWNUM = 1
                        AND K.SITAFA <> 7
                        AND K.ESTPOS = K.ESTPOS
                        AND K.POSTRA = (
                        SELECT
                            Z.POSTRA
                        FROM
                            senior.R017HIE Z
                        WHERE
                            Z.ESTPOS = FUN.ESTPOS
                            AND ROWNUM <= 1
                            AND Z.POSPOS = (
                            SELECT
                                SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                            FROM
                                senior.R017HIE HIE
                            WHERE
                                HIE.ESTPOS = FUN.ESTPOS
                                AND HIE.POSTRA = FUN.POSTRA
                                AND ROWNUM <= 1
                            )
                    )
                ) AS USERSUP
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
                    AND FUN.TIPCOL = '1'
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