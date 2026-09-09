class Professor:
    def __init__(
        self, codigo: int = 0, nome: str = "", endereco: str = "", telefone: str = ""
    ):
        self.__codigo = codigo
        self.__nome = nome
        self.__endereco = endereco
        self.__telefone = telefone

    @property
    def codigo(self):
        return self.__codigo

    @property
    def nome(self):
        return self.__nome

    @property
    def endereco(self):
        return self.__endereco

    @property
    def telefone(self):
        return self.__telefone
