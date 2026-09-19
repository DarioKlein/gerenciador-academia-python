from repositories import Repositorio, TipoRepositorio
from models import Professor


class ProfessorService:
    def __init__(self, repositorio_professores: Repositorio):
        if not isinstance(repositorio_professores, Repositorio):
            raise TypeError("O repositório informado é inválido")

        if repositorio_professores.tipo != TipoRepositorio.PROFESSOR:
            raise ValueError("O repositório informado não é de professores")

        self.__repositorio_professores = repositorio_professores

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

        self.__repositorio_professores.atualizar(codigo, professor_atualizado.para_dict())

        return professor_atualizado

    def excluir(self, codigo: int) -> Professor:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro_excluido = self.__repositorio_professores.excluir(codigo)

        return Professor.dict_para_objeto(registro_excluido)
