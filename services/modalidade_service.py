from repositories import Repositorio, TipoRepositorio
from models import Modalidade, Professor


class ModalidadeService:

    def __init__(
        self,
        repositorio_modalidades: Repositorio,
        repositorio_professores: Repositorio,
        repositorio_matriculas: Repositorio,
    ):
        if not isinstance(repositorio_modalidades, Repositorio):
            raise TypeError("O repositório de modalidades informado é inválido")

        if not isinstance(repositorio_professores, Repositorio):
            raise TypeError("O repositório de professores informado é inválido")

        if not isinstance(repositorio_matriculas, Repositorio):
            raise TypeError("O repositório de matrículas informado é inválido")

        if repositorio_modalidades.tipo != TipoRepositorio.MODALIDADE:
            raise ValueError("O repositório informado não é de modalidades")

        if repositorio_professores.tipo != TipoRepositorio.PROFESSOR:
            raise ValueError("O repositório informado não é de professores")

        if repositorio_matriculas.tipo != TipoRepositorio.MATRICULA:
            raise ValueError("O repositório informado não é de matrículas")

        self.__repositorio_modalidades = repositorio_modalidades
        self.__repositorio_professores = repositorio_professores
        self.__repositorio_matriculas = repositorio_matriculas

    def criar(self, modalidade: Modalidade) -> Modalidade:
        if not isinstance(modalidade, Modalidade):
            raise TypeError("A modalidade informada é inválida")

        if self.__repositorio_professores.buscar(modalidade.cod_prof) is None:
            raise ValueError("O professor informado não foi encontrado")

        self.__repositorio_modalidades.incluir(modalidade.para_dict())
        return modalidade

    def buscar(self, codigo: int) -> tuple[Modalidade, Professor] | None:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro_modalidade = self.__repositorio_modalidades.buscar(codigo)

        if registro_modalidade is None:
            return None

        modalidade = Modalidade.dict_para_objeto(registro_modalidade)

        registro_professor = self.__repositorio_professores.buscar(modalidade.cod_prof)

        if registro_professor is None:
            raise ValueError("O professor relacionado à modalidade não foi encontrado")

        professor = Professor.dict_para_objeto(registro_professor)

        return modalidade, professor

    def atualizar(self, codigo: int, modalidade_atualizada: Modalidade) -> Modalidade:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if not isinstance(modalidade_atualizada, Modalidade):
            raise TypeError("A modalidade informada é inválida")

        if (
            self.__repositorio_professores.buscar(modalidade_atualizada.cod_prof)
            is None
        ):
            raise ValueError("O professor informado não foi encontrado")

        self.__repositorio_modalidades.atualizar(
            codigo, modalidade_atualizada.para_dict()
        )

        return modalidade_atualizada

    def excluir(self, codigo: int) -> Modalidade:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if self.__buscar_matricula(codigo):
            raise ValueError(
                "A modalidade informada possui vínculo a uma matrícula, portanto para excluí-la você deve primeiro excluir sua matrícula."
            )

        registro_excluido = self.__repositorio_modalidades.excluir(codigo)

        return Modalidade.dict_para_objeto(registro_excluido)

    def buscar_professor(self, codigo: int) -> Professor | None:
        if not isinstance(codigo, int):
            raise TypeError("O código do professor informado é inválido")

        registro = self.__repositorio_professores.buscar(codigo)

        if registro is None:
            return None

        return Professor.dict_para_objeto(registro)

    def __buscar_matricula(self, cod_modalidade: int) -> bool:
        for registro in self.__repositorio_matriculas.listar():
            if registro["cod_modalidade"] == cod_modalidade:
                return True

        return False
