class Matricula:
    def __init__(
        self, codigo: int, cod_aluno: int, cod_modalidade: int, qtde_aulas: int
    ):
        self.__codigo = codigo
        self.__cod_aluno = cod_aluno
        self.__cod_modalidade = cod_modalidade
        self.__qtde_aulas = qtde_aulas
