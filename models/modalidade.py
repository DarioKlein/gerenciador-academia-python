class Modalidade:
    def __init__(
        self,
        codigo: int = 0,
        descricao: str = "",
        cod_prof: int = 0,
        valor_aula: float = 0.0,
        limite_alunos: int = 0,
        total_alunos: int = 0,
    ):
        self.__codigo = codigo
        self.__descricao = descricao
        self.__cod_prof = cod_prof
        self.__valor_aula = valor_aula
        self.__limite_alunos = limite_alunos
        self.__total_alunos = total_alunos

    @property
    def codigo(self):
        return self.__codigo

    @property
    def descricao(self):
        return self.__descricao

    @property
    def cod_prof(self):
        return self.__cod_prof

    @property
    def valor_aula(self):
        return self.__valor_aula

    @property
    def limite_alunos(self):
        return self.__limite_alunos

    @property
    def total_alunos(self):
        return self.__total_alunos
