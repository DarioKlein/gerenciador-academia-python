from utils import Validador


class Professor:
    def __init__(self, codigo: int, nome: str, endereco: str, telefone: str):
        self.codigo = codigo
        self.nome = nome
        self.endereco = endereco
        self.telefone = telefone

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
    def endereco(self):
        return self.__endereco

    @endereco.setter
    def endereco(self, endereco):
        if endereco is None:
            raise ValueError("O endereço é obrigatório")

        if not isinstance(endereco, str):
            raise TypeError("O endereço deve ser do tipo texto")

        endereco = endereco.strip()

        if not endereco:
            raise ValueError("O endereço não pode estar vazio")

        self.__endereco = endereco

    @property
    def telefone(self):
        return self.__telefone

    @telefone.setter
    def telefone(self, telefone):
        if telefone is None:
            raise ValueError("O telefone é obrigatório")

        if not isinstance(telefone, str):
            raise TypeError("O telefone deve ser do tipo texto")

        telefone = telefone.strip()

        if not telefone:
            raise ValueError("O telefone não pode estar vazio")

        if not telefone.isnumeric():
            raise ValueError("O telefone deve conter apenas números")

        if len(telefone) != 11:
            raise ValueError("O número de telefone digitado é inválido")

        self.__telefone = telefone
