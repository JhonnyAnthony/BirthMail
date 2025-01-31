from connectionDB import Database

class Querys:
    def __init__(self):
        self.db = Database()
        self.db.connectData()

    def r034fun(self):
        queryFun = """ 
                SELECT
                    NUMCAD AS NUMCAD,
                    DATADM AS DATADM,
                    DATNAS AS DATNAS,
                    NOMFUN AS NOMFUN,
                    CODCAR AS CODCAR,
                    NUMLOC AS NUMLOC,
                    POSTRA
                FROM
                    SENIOR.R034FUN 
                WHERE
                    SITAFA = '1'
                    AND TIPCOL = '1'
                """
        return queryFun

    def r034cpl(self):
        queryEm = """
                SELECT
                    NUMEMP,
                    TIPCOL,
                    NUMCAD,
                    EMAPAR
                FROM
                    SENIOR.R034CPL
                """
        return queryEm

    def r999usu(self):
        queryUsu = """
                SELECT
                    CODUSU,
                    NOMUSU,
                    NUMCAD
                FROM
                    SENIOR.R999USU
                """
        return queryUsu

    def r024car(self):
        queryCar = """
                SELECT
                    ESTCAR,
                    CODCAR,
                    TITCAR
                FROM
                    SENIOR.R024CAR
                """
        return queryCar

    def r016orn(self):
        queryOrn = """
                SELECT
                    NUMLOC,
                    NOMLOC
                FROM
                    SENIOR.R016ORN
                """
        return queryOrn

    def get_postra_che(self, estpos, postra):
        queryPostraChe = """
                    SELECT Z.POSTRA
                    FROM senior.R017HIE Z
                    WHERE Z.ESTPOS = {}
                    AND Z.POSPOS = (
                        SELECT SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                        FROM senior.R017HIE HIE
                        WHERE HIE.ESTPOS = {}
                        AND HIE.POSTRA = {}
                    )
                    """.format(estpos, estpos, postra)
        return queryPostraChe

    def get_idepos(self, estpos, postra):
        queryIdePos = """
                    SELECT Z.IDEPOS
                    FROM senior.R017HIE Z
                    WHERE Z.ESTPOS = {}
                    AND Z.POSPOS = (
                        SELECT SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                        FROM senior.R017HIE HIE
                        WHERE HIE.ESTPOS = {}
                        AND HIE.POSTRA = {}
                    )
                    """.format(estpos, estpos, postra)
        return queryIdePos

    def get_nomesup(self, estpos, postra):
        queryNomeSup = """
                    SELECT K.NOMFUN
                    FROM senior.R034FUN K
                    WHERE K.ESTPOS = {}
                    AND K.POSTRA = (
                        SELECT Z.POSTRA
                        FROM senior.R017HIE Z
                        WHERE Z.ESTPOS = {}
                        AND Z.POSPOS = (
                            SELECT SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                            FROM senior.R017HIE HIE
                            WHERE HIE.ESTPOS = {}
                            AND HIE.POSTRA = {}
                        )
                    )
                    """.format(estpos, estpos, estpos, postra, postra)
        return queryNomeSup

    def get_usersup(self, estpos, postra):
        queryUserSup = """
                    SELECT SUP.NOMUSU
                    FROM senior.R034FUN K
                    INNER JOIN senior.R034USU F ON K.NUMEMP = F.NUMEMP AND K.TIPCOL = F.TIPCOL AND K.NUMCAD = F.NUMCAD
                    INNER JOIN senior.R999USU SUP ON F.CODUSU = SUP.CODUSU
                    WHERE K.ESTPOS = {}
                    AND K.POSTRA = (
                        SELECT Z.POSTRA
                        FROM senior.R017HIE Z
                        WHERE Z.ESTPOS = {}
                        AND Z.POSPOS = (
                            SELECT SUBSTR(POSPOS, 0, LENGTH(POSPOS)-2)
                            FROM senior.R017HIE HIE
                            WHERE HIE.ESTPOS = {}
                            AND HIE.POSTRA = {}
                        )
                    )
                    """.format(estpos, estpos, estpos, postra, postra)
        return queryUserSup