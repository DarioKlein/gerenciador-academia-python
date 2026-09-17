from repositories import Repositorio, TipoRepositorio
from models import Aluno


class AlunoService:
    def __init__(self, repositorio_alunos: Repositorio):
        if not isinstance(repositorio_alunos, Repositorio):
            raise TypeError("O repositório informado é inválido")

        if repositorio_alunos.tipo != TipoRepositorio.ALUNO:
            raise ValueError("O repositório informado não é de alunos")

        self.repositorio_alunos = repositorio_alunos

    def criar(self, aluno: Aluno) -> Aluno:
        if not isinstance(aluno, Aluno):
            raise TypeError("O aluno informado é inválido")

        self.repositorio_alunos.incluir(aluno.para_dict())
        return aluno

    def buscar(self, codigo: int) -> Aluno | None:
        if not isinstance(codigo, int):
            raise TypeError("O codigo informado é inválido")

        registro = self.repositorio_alunos.buscar(codigo)

        if registro is None:
            return None

        return Aluno.de_dict(registro)

    def atualizar(self, codigo: int, aluno_atualizado: Aluno) -> Aluno:
        if not isinstance(codigo, int):
            raise TypeError("O codigo informado é inválido")

        if not isinstance(aluno_atualizado, Aluno):
            raise TypeError("O aluno informado é inválido")

        self.repositorio_alunos.atualizar(codigo, aluno_atualizado.para_dict())

        return aluno_atualizado

    def excluir(self, codigo: int) -> Aluno:
        if not isinstance(codigo, int):
            raise TypeError("O codigo informado é inválido")

        registro_excluido = self.repositorio_alunos.excluir(codigo)
        return Aluno.de_dict(registro_excluido)
