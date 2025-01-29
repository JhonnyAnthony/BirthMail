from connectionDB import Database
class Querys:
    def __init__(self):
        self.db = Database()
        self.db.connectData()
    def r034fun():
        queryFun=""" 
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
    def r034cpl():
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
    def r999usu():
        queryUsu="""
                SELECT
                    CODUSU,
                    NOMUSU,
                    NUMCAD,
                FROM
                    SENIOR.R999USU
                """
        return queryUsu
    def  r024car():
        queryCar = """
                SELECT
                    ESTCAR,
                    CODCAR,
                    TITCAR
                FROM
                    SENIOR.R024CAR
                """
        return queryCar
    def r016orn():
        queryOrn = """
                SELECT
                    NUMLOC,
                    NOMLOC
                FROM
                    SENIOR.R016ORN
                    """
        return queryOrn
    def superior():
        querySUP="""
        SELECT
                    --Local
                    FUN.NOMFUN,
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
                        Z.IDEPOS
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
                ) AS IDEPOS,
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
                    AND (
                    SELECT
                        Z.POSTRA
                    FROM
                        senior.R017HIE Z
                    WHERE
                        Z.ESTPOS = FUN.ESTPOS
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
                        AND ROWNUM <= 1) IS NOT NULL"""
        return querySUP
    def queryAll():
        query = """
            SELECT
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
                FUN.NUMLOC AS NUMLOC,
                --Local
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
                    Z.IDEPOS
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
            ) AS IDEPOS,
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
                AND (
                SELECT
                    Z.POSTRA
                FROM
                    senior.R017HIE Z
                WHERE
                    Z.ESTPOS = FUN.ESTPOS
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
                    AND ROWNUM <= 1) IS NOT NULL
                    """
        return query
    