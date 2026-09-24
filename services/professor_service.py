from repositories import Repositorio, TipoRepositorio
from models import Professor


class ProfessorService:
    def __init__(
        self, repositorio_professores: Repositorio, repositorio_modalidades: Repositorio
    ):
        if not isinstance(repositorio_professores, Repositorio):
            raise TypeError("O repositório de professores informado é inválido")

        if not isinstance(repositorio_modalidades, Repositorio):
            raise TypeError("O repositório de modalidades informado é inválido")

        if repositorio_professores.tipo != TipoRepositorio.PROFESSOR:
            raise ValueError("O repositório informado não é de professores")

        if repositorio_modalidades.tipo != TipoRepositorio.MODALIDADE:
            raise ValueError("O repositório informado não é de modalidades")

        self.__repositorio_professores = repositorio_professores
        self.__repositorio_modalidades = repositorio_modalidades

    def listar(self) -> list[Professor]:
        professores = []

        professores_dict = self.__repositorio_professores.listar()

        for professor in professores_dict:
            professores.append(Professor.dict_para_objeto(professor))

        return professores

    def criar(self, professor: Professor) -> Professor:
        if not isinstance(professor, Professor):
            raise TypeError("O professor informado é inválido")

        self.__repositorio_professores.incluir(professor.para_dict())
        return professor

    def buscar(self, codigo: int) -> Professor | None:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro = self.__repositorio_professores.buscar(codigo)

        if registro is None:
            return None

        return Professor.dict_para_objeto(registro)

    def atualizar(self, codigo: int, professor_atualizado: Professor) -> Professor:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if not isinstance(professor_atualizado, Professor):
            raise TypeError("O professor informado é inválido")

        self.__repositorio_professores.atualizar(
            codigo, professor_atualizado.para_dict()
        )

        return professor_atualizado

    def excluir(self, codigo: int) -> Professor:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if self.__buscar_modalidade(codigo):
            raise ValueError(
                "O professor informado está vinculado a uma modalidade, portanto para excluí-lo você deve primeiro excluir sua modalidade."
            )

        registro_excluido = self.__repositorio_professores.excluir(codigo)

        return Professor.dict_para_objeto(registro_excluido)

    def __buscar_modalidade(self, cod_professor: int) -> bool:
        for registro in self.__repositorio_modalidades.listar():
            if registro["cod_prof"] == cod_professor:
                return True

        return False
