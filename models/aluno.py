from datetime import date


class Aluno:
    def __init__(
        self, codigo: int, nome: str, data_nascimento: date, peso: float, altura: float
    ):
        self.__codigo = codigo
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__peso = peso
        self.__altura = altura
