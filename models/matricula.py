class Matricula:
    def __init__(
        self,
        codigo: int,
        cod_aluno: int,
        cod_modalidade: int,
        qtde_aulas: int,
    ):
        self.codigo = codigo
        self.cod_aluno = cod_aluno
        self.cod_modalidade = cod_modalidade
        self.qtde_aulas = qtde_aulas

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo):
        if codigo is None:
            raise ValueError("O código é obrigatório")

        if not isinstance(codigo, int):
            raise TypeError("O código deve ser um número inteiro.")

        if codigo <= 0:
            raise ValueError("O código deve ser um valor a partir de 1")

        self.__codigo = codigo

    @property
    def cod_aluno(self):
        return self.__cod_aluno

    @cod_aluno.setter
    def cod_aluno(self, cod_aluno):
        if cod_aluno is None:
            raise ValueError("O código do aluno é obrigatório")

        if not isinstance(cod_aluno, int):
            raise TypeError("O código do aluno deve ser um número inteiro.")

        if cod_aluno <= 0:
            raise ValueError("O código do aluno deve ser um valor a partir de 1")

        self.__cod_aluno = cod_aluno

    @property
    def cod_modalidade(self):
        return self.__cod_modalidade

    @cod_modalidade.setter
    def cod_modalidade(self, cod_modalidade):
        if cod_modalidade is None:
            raise ValueError("O código da modalidade é obrigatório")

        if not isinstance(cod_modalidade, int):
            raise TypeError("O código da modalidade deve ser um número inteiro.")

        if cod_modalidade <= 0:
            raise ValueError("O código da modalidade deve ser um valor a partir de 1")

        self.__cod_modalidade = cod_modalidade

    @property
    def qtde_aulas(self):
        return self.__qtde_aulas

    @qtde_aulas.setter
    def qtde_aulas(self, qtde_aulas):
        if qtde_aulas is None:
            raise ValueError("A quantidade de aulas é obrigatória")

        if not isinstance(qtde_aulas, int):
            raise TypeError("A quantidade de aulas deve ser um número inteiro")

        if qtde_aulas <= 0:
            raise ValueError("A quantidade de aulas deve ser maior que zero")

        self.__qtde_aulas = qtde_aulas
