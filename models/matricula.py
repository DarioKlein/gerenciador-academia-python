class Matricula:
    def __init__(
        self,
        codigo: int = 0,
        cod_aluno: int = 0,
        cod_modalidade: int = 0,
        qtde_aulas: int = 0,
    ):
        self.__codigo = codigo
        self.__cod_aluno = cod_aluno
        self.__cod_modalidade = cod_modalidade
        self.__qtde_aulas = qtde_aulas

    @property
    def codigo(self):
        return self.__codigo

    @property
    def cod_aluno(self):
        return self.__cod_aluno

    @property
    def cod_modalidade(self):
        return self.__cod_modalidade

    @property
    def qtde_aulas(self):
        return self.__qtde_aulas
