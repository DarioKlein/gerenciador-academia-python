from repositories import Repositorio, TipoRepositorio
from models import Matricula, Aluno, Modalidade


class MatriculaService:

    def __init__(
        self,
        repositorio_matriculas: Repositorio,
        repositorio_alunos: Repositorio,
        repositorio_modalidades: Repositorio,
    ):
        if not isinstance(repositorio_matriculas, Repositorio):
            raise TypeError("O repositório de matrículas informado é inválido")

        if not isinstance(repositorio_alunos, Repositorio):
            raise TypeError("O repositório de alunos informado é inválido")

        if not isinstance(repositorio_modalidades, Repositorio):
            raise TypeError("O repositório de modalidades informado é inválido")

        if repositorio_matriculas.tipo != TipoRepositorio.MATRICULA:
            raise ValueError("O repositório informado não é de matrículas")

        if repositorio_alunos.tipo != TipoRepositorio.ALUNO:
            raise ValueError("O repositório informado não é de alunos")

        if repositorio_modalidades.tipo != TipoRepositorio.MODALIDADE:
            raise ValueError("O repositório informado não é de modalidades")

        self.__repositorio_matriculas = repositorio_matriculas
        self.__repositorio_alunos = repositorio_alunos
        self.__repositorio_modalidades = repositorio_modalidades

    def criar(self, matricula: Matricula) -> Matricula:
        if not isinstance(matricula, Matricula):
            raise TypeError("A matrícula informada é inválida")

        if self.__repositorio_alunos.buscar(matricula.cod_aluno) is None:
            raise ValueError("O aluno informado não foi encontrado")

        registro_modalidade = self.__repositorio_modalidades.buscar(
            matricula.cod_modalidade
        )

        if registro_modalidade is None:
            raise ValueError("A modalidade informada não foi encontrada")

        if registro_modalidade["total_alunos"] >= registro_modalidade["limite_alunos"]:
            raise ValueError(
                "A modalidade informada não possui vagas disponíveis para matrícula"
            )

        self.__repositorio_matriculas.incluir(matricula.para_dict())

        registro_modalidade["total_alunos"] += 1

        self.__repositorio_modalidades.atualizar(
            registro_modalidade["codigo"], registro_modalidade
        )

        return matricula

    def buscar(self, codigo: int) -> tuple[Matricula, Aluno, Modalidade] | None:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro_matricula = self.__repositorio_matriculas.buscar(codigo)

        if registro_matricula is None:
            return None

        matricula = Matricula.dict_para_objeto(registro_matricula)

        registro_aluno = self.__repositorio_alunos.buscar(matricula.cod_aluno)

        if registro_aluno is None:
            raise ValueError("O aluno relacionado à matrícula não foi encontrado")

        aluno = Aluno.dict_para_objeto(registro_aluno)

        registro_modalidade = self.__repositorio_modalidades.buscar(
            matricula.cod_modalidade
        )

        if registro_modalidade is None:
            raise ValueError("A modalidade relacionada à matrícula não foi encontrada")

        modalidade = Modalidade.dict_para_objeto(registro_modalidade)

        return matricula, aluno, modalidade

    def atualizar(self, codigo: int, matricula_atualizada: Matricula) -> Matricula:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if not isinstance(matricula_atualizada, Matricula):
            raise TypeError("A matrícula informada é inválida")

        if self.__repositorio_alunos.buscar(matricula_atualizada.cod_aluno) is None:
            raise ValueError("O aluno informado não foi encontrado")

        if (
            self.__repositorio_modalidades.buscar(matricula_atualizada.cod_modalidade)
            is None
        ):
            raise ValueError("A modalidade informada não foi encontrada")

        self.__repositorio_matriculas.atualizar(
            codigo, matricula_atualizada.para_dict()
        )

        return matricula_atualizada

    def excluir(self, codigo: int) -> Matricula:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro_matricula = self.__repositorio_matriculas.buscar(codigo)

        if registro_matricula is None:
            raise ValueError("A matrícula informada não foi encontrada")

        registro_modalidade = self.__repositorio_modalidades.buscar(
            registro_matricula["cod_modalidade"]
        )

        if registro_modalidade is None:
            raise ValueError("A modalidade relacionada à matrícula não foi encontrada")

        self.__repositorio_matriculas.excluir(codigo)

        registro_modalidade["total_alunos"] -= 1

        self.__repositorio_modalidades.atualizar(
            registro_modalidade["codigo"], registro_modalidade
        )

        return Matricula.dict_para_objeto(registro_matricula)
