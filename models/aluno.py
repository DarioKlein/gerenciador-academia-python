from datetime import date
from utils import Validador


class Aluno:

    def __init__(
        self,
        codigo: int,
        nome: str,
        data_nascimento: date,
        peso: float,
        altura: float,
    ):
        self.codigo = codigo
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.peso = peso
        self.altura = altura

    @property
    def codigo(self):
        return self.__codigo

    @codigo.setter
    def codigo(self, codigo: int):
        if codigo is None:
            raise ValueError("O codigo é obrigatório")

        if not isinstance(codigo, int):
            raise TypeError("O código deve ser um número inteiro.")

        if codigo <= 0:
            raise ValueError("O código deve ser um valor a partir de 1")

        self.__codigo = codigo

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, nome: str):
        if nome is None:
            raise ValueError("O nome é obrigatório")

        if not isinstance(nome, str):
            raise TypeError("O nome deve ser do tipo texto")

        nome = nome.strip()

        if not nome:
            raise ValueError("O nome não pode estar vazio")

        if not Validador.texto_e_valido(nome):
            raise ValueError("Nome inválido: use apenas letras e espaços")

        self.__nome = nome

    @property
    def data_nascimento(self):
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento):
        if data_nascimento is None:
            raise ValueError("A data de nascimento é obrigatória")

        if not isinstance(data_nascimento, date):
            raise TypeError("A data de nascimento deve ser do tipo data")

        if data_nascimento.year > date.today().year - 14:
            raise ValueError("Idade mínima não atingida")

        if data_nascimento < date(1900, 1, 1):
            raise ValueError(
                "A data de nascimento não pode ser mais antiga do que 01/01/1900"
            )

        self.__data_nascimento = data_nascimento

    @property
    def peso(self):
        return self.__peso

    @peso.setter
    def peso(self, peso):
        if peso is None:
            raise ValueError("O peso é obrigatório")

        if not isinstance(peso, (int, float)):
            raise TypeError("O peso deve ser do tipo numérico")

        if peso <= 0:
            raise ValueError("O peso deve ser maior que zero")

        self.__peso = float(peso)

    @property
    def altura(self):
        return self.__altura

    @altura.setter
    def altura(self, altura):
        if altura is None:
            raise ValueError("A altura é obrigatória")

        if not isinstance(altura, (int, float)):
            raise TypeError("A altura deve ser um valor numérico")

        if altura <= 0:
            raise ValueError("A altura deve ser maior que zero")

        if altura > 3:
            raise ValueError("A altura deve ser informada em metros")

        self.__altura = float(altura)
