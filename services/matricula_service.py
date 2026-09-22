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

        if self.__aluno_ja_matriculado(
            matricula.cod_aluno,
            matricula.cod_modalidade,
        ):
            raise ValueError("O aluno já está matriculado nesta modalidade")

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

        registro_matricula_antiga = self.__repositorio_matriculas.buscar(codigo)

        if registro_matricula_antiga is None:
            raise ValueError("A matrícula informada não existe")

        if registro_matricula_antiga["cod_aluno"] != matricula_atualizada.cod_aluno:
            raise ValueError("O aluno de uma matrícula não pode ser alterado")

        if self.__repositorio_alunos.buscar(matricula_atualizada.cod_aluno) is None:
            raise ValueError("O aluno informado não foi encontrado")

        registro_modalidade_antiga = self.__repositorio_modalidades.buscar(
            registro_matricula_antiga["cod_modalidade"]
        )

        if registro_modalidade_antiga is None:
            raise ValueError("A modalidade da matrícula em questão não existe mais")

        modalidade_foi_alterada = (
            registro_matricula_antiga["cod_modalidade"]
            != matricula_atualizada.cod_modalidade
        )

        if modalidade_foi_alterada:
            registro_modalidade_nova = self.__repositorio_modalidades.buscar(
                matricula_atualizada.cod_modalidade
            )

            if registro_modalidade_nova is None:
                raise ValueError("A modalidade informada não foi encontrada")

            if self.__aluno_ja_matriculado(
                matricula_atualizada.cod_aluno,
                matricula_atualizada.cod_modalidade,
                codigo_ignorado=codigo,
            ):
                raise ValueError("O aluno já está matriculado nesta modalidade")

            if (
                registro_modalidade_nova["total_alunos"]
                >= registro_modalidade_nova["limite_alunos"]
            ):
                raise ValueError(
                    "A modalidade informada não possui vagas disponíveis para matrícula"
                )

        self.__repositorio_matriculas.atualizar(
            codigo, matricula_atualizada.para_dict()
        )

        if modalidade_foi_alterada:
            registro_modalidade_nova["total_alunos"] += 1
            registro_modalidade_antiga["total_alunos"] -= 1

            self.__repositorio_modalidades.atualizar(
                registro_modalidade_nova["codigo"], registro_modalidade_nova
            )

            self.__repositorio_modalidades.atualizar(
                registro_modalidade_antiga["codigo"], registro_modalidade_antiga
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

    def __aluno_ja_matriculado(
        self,
        cod_aluno: int,
        cod_modalidade: int,
        codigo_ignorado: int | None = None,
    ) -> bool:
        for registro in self.__repositorio_matriculas.listar():
            if registro["codigo"] == codigo_ignorado:
                continue

            if (
                registro["cod_aluno"] == cod_aluno
                and registro["cod_modalidade"] == cod_modalidade
            ):
                return True

        return False

    def buscar_aluno(self, codigo: int) -> Aluno | None:
        if not isinstance(codigo, int):
            raise TypeError("O código do aluno informado é inválido")

        registro = self.__repositorio_alunos.buscar(codigo)

        if registro is None:
            return None

        return Aluno.dict_para_objeto(registro)

    def buscar_modalidade(self, codigo: int) -> Modalidade | None:
        if not isinstance(codigo, int):
            raise TypeError("O código da modalidade informado é inválido")

        registro = self.__repositorio_modalidades.buscar(codigo)

        if registro is None:
            return None

        return Modalidade.dict_para_objeto(registro)
