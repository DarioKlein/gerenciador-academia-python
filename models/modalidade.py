from utils import Validador


class Modalidade:
    def __init__(
        self,
        codigo: int,
        descricao: str,
        cod_prof: int,
        valor_aula: float,
        limite_alunos: int,
        total_alunos: int,
    ):
        self.codigo = codigo
        self.descricao = descricao
        self.cod_prof = cod_prof
        self.valor_aula = valor_aula
        self.limite_alunos = limite_alunos
        self.total_alunos = total_alunos

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
    def descricao(self):
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str):
        if descricao is None:
            raise ValueError("A descrição é obrigatória")

        if not isinstance(descricao, str):
            raise TypeError("A descrição deve ser do tipo texto")

        descricao = descricao.strip()

        if not descricao:
            raise ValueError("A descrição não pode estar vazia")

        if not Validador.texto_e_valido(descricao):
            raise ValueError("Descrição inválida: use apenas letras e espaços")

        self.__descricao = descricao

    @property
    def cod_prof(self):
        return self.__cod_prof

    @cod_prof.setter
    def cod_prof(self, cod_prof):
        if cod_prof is None:
            raise ValueError("O código do professor é obrigatório")

        if not isinstance(cod_prof, int):
            raise TypeError("O código do professor deve ser um número inteiro.")

        if cod_prof <= 0:
            raise ValueError("O código do professor deve ser um valor a partir de 1")

        self.__cod_prof = cod_prof

    @property
    def valor_aula(self):
        return self.__valor_aula

    @valor_aula.setter
    def valor_aula(self, valor_aula):
        if valor_aula is None:
            raise ValueError("O valor da aula é obrigatório")

        if not isinstance(valor_aula, (int, float)):
            raise TypeError("O valor da aula deve ser um valor numérico")

        if valor_aula <= 0:
            raise ValueError("O valor da aula deve ser maior que zero")

        self.__valor_aula = float(valor_aula)

    @property
    def limite_alunos(self):
        return self.__limite_alunos

    @limite_alunos.setter
    def limite_alunos(self, limite_alunos):
        if limite_alunos is None:
            raise ValueError("O limite de alunos é obrigatório")

        if not isinstance(limite_alunos, int):
            raise TypeError("O limite de alunos deve ser um número inteiro")

        if limite_alunos <= 0:
            raise ValueError("O limite de alunos deve ser maior que zero")

        self.__limite_alunos = limite_alunos

    @property
    def total_alunos(self):
        return self.__total_alunos

    @total_alunos.setter
    def total_alunos(self, total_alunos):
        if total_alunos is None:
            raise ValueError("O total de alunos é obrigatório")

        if not isinstance(total_alunos, int):
            raise TypeError("O total de alunos deve ser um número inteiro")

        if total_alunos < 0:
            raise ValueError("O total de alunos não pode ser negativo")

        if total_alunos > self.__limite_alunos:
            raise ValueError(
                "O total de alunos deve ser menor ou igual ao limite de alunos"
            )

        self.__total_alunos = total_alunos
