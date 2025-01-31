# testaquery.py

from importaDados import Querys

class TestQueries:
    def __init__(self):
        self.db = Querys().db  # Usa a instância do banco de dados da classe Querys
        self.queries = Querys()

    def test_r034fun(self):
        query = self.queries.r034fun()
        result = self.db.executeQuery(query)
        print("Result for r034fun:", result)  # Adicionado para imprimir o resultado
        assert len(result) > 0, "Query r034fun returned no results"

    def test_r034cpl(self):
        query = self.queries.r034cpl()
        result = self.db.executeQuery(query)
        print("Result for r034cpl:", result)  # Adicionado para imprimir o resultado
        assert len(result) > 0, "Query r034cpl returned no results"

    def test_r999usu(self):
        query = self.queries.r999usu()
        result = self.db.executeQuery(query)
        print("Result for r999usu:", result)  # Adicionado para imprimir o resultado
        assert len(result) > 0, "Query r999usu returned no results"

    def test_r024car(self):
        query = self.queries.r024car()
        result = self.db.executeQuery(query)
        print("Result for r024car:", result)  # Adicionado para imprimir o resultado
        assert len(result) > 0, "Query r024car returned no results"

    def test_r016orn(self):
        query = self.queries.r016orn()
        result = self.db.executeQuery(query)
        print("Result for r016orn:", result)  # Adicionado para imprimir o resultado
        assert len(result) > 0, "Query r016orn returned no results"

# Para executar os testes
if __name__ == "__main__":
    tester = TestQueries()
    tester.test_r034fun()
    tester.test_r034cpl()
    tester.test_r999usu()
    tester.test_r024car()
    tester.test_r016orn()
    print("All tests passed successfully!")
