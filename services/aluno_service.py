from repositories import Repositorio, TipoRepositorio
from models import Aluno


class AlunoService:

    def __init__(
        self, repositorio_alunos: Repositorio, repositorio_matriculas: Repositorio
    ):
        if not isinstance(repositorio_alunos, Repositorio):
            raise TypeError("O repositório de alunos informado é inválido")

        if not isinstance(repositorio_matriculas, Repositorio):
            raise TypeError("O repositório de matrículas informado é inválido")

        if repositorio_alunos.tipo != TipoRepositorio.ALUNO:
            raise ValueError("O repositório informado não é de alunos")

        if repositorio_matriculas.tipo != TipoRepositorio.MATRICULA:
            raise ValueError("O repositório informado não é de matrículas")

        self.__repositorio_alunos = repositorio_alunos
        self.__repositorio_matriculas = repositorio_matriculas

    def criar(self, aluno: Aluno) -> Aluno:
        if not isinstance(aluno, Aluno):
            raise TypeError("O aluno informado é inválido")

        self.__repositorio_alunos.incluir(aluno.para_dict())
        return aluno

    def buscar(self, codigo: int) -> Aluno | None:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro = self.__repositorio_alunos.buscar(codigo)

        if registro is None:
            return None

        return Aluno.dict_para_objeto(registro)

    def atualizar(self, codigo: int, aluno_atualizado: Aluno) -> Aluno:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if not isinstance(aluno_atualizado, Aluno):
            raise TypeError("O aluno informado é inválido")

        self.__repositorio_alunos.atualizar(codigo, aluno_atualizado.para_dict())

        return aluno_atualizado

    def excluir(self, codigo: int) -> Aluno:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if self.__buscar_matricula(codigo):
            raise ValueError(
                "O aluno informado possui uma matrícula, portanto para excluí-lo você deve primeiro excluir sua matrícula."
            )

        registro_excluido = self.__repositorio_alunos.excluir(codigo)

        return Aluno.dict_para_objeto(registro_excluido)

    def __buscar_matricula(self, cod_aluno: int) -> bool:
        for registro in self.__repositorio_matriculas.listar():
            if registro["cod_aluno"] == cod_aluno:
                return True

        return False
