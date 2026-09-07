class Modalidade:
    def __init__(
        self,
        codigo: int,
        descricao: str,
        cod_prof: int,
        valor_aula: float,
        limite_alunos: float,
        total_alunos: float,
    ):
        self.__codigo = codigo
        self.__descricao = descricao
        self.__cod_prof = cod_prof
        self.__valor_aula = valor_aula
        self.__limite_alunos = limite_alunos
        self.__total_alunos = total_alunos
