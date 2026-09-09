from datetime import date
from typing import Optional


class Aluno:

    def __init__(
        self,
        codigo: int = 0,
        nome: str = "",
        data_nascimento: Optional[date] = None,
        peso: float = 0.0,
        altura: float = 0.0,
    ):
        self.__codigo = codigo
        self.__nome = nome
        self.__data_nascimento = data_nascimento if data_nascimento else date.today()
        self.__peso = peso
        self.__altura = altura

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nome(self):
        return self.__nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @property
    def peso(self):
        return self.__peso

    @property
    def altura(self):
        return self.__altura
