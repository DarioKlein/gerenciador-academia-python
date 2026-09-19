from repositories import Repositorio, TipoRepositorio
from models import Matricula


# Falta implementar as regras de negócio e validar o código de aluno e modalidade
class MatriculaService:

    def __init__(self, repositorio_matriculas: Repositorio):
        if not isinstance(repositorio_matriculas, Repositorio):
            raise TypeError("O repositório informado é inválido")

        if repositorio_matriculas.tipo != TipoRepositorio.MATRICULA:
            raise ValueError("O repositório informado não é de matrículas")

        self.__repositorio_matriculas = repositorio_matriculas

    def criar(self, matricula: Matricula) -> Matricula:
        if not isinstance(matricula, Matricula):
            raise TypeError("A matrícula informada é inválida")

        self.__repositorio_matriculas.incluir(matricula.para_dict())
        return matricula

    def buscar(self, codigo: int) -> Matricula | None:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro = self.__repositorio_matriculas.buscar(codigo)

        if registro is None:
            return None

        return Matricula.dict_para_objeto(registro)

    def atualizar(self, codigo: int, matricula_atualizada: Matricula) -> Matricula:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if not isinstance(matricula_atualizada, Matricula):
            raise TypeError("A matrícula informada é inválida")

        self.__repositorio_matriculas.atualizar(
            codigo, matricula_atualizada.para_dict()
        )

        return matricula_atualizada

    def excluir(self, codigo: int) -> Matricula:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro_excluido = self.__repositorio_matriculas.excluir(codigo)

        return Matricula.dict_para_objeto(registro_excluido)
