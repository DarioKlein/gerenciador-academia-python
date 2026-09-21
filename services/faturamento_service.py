from .modalidade_service import ModalidadeService
from repositories import Repositorio, TipoRepositorio
from models import Modalidade, Professor


class FaturamentoService:
    def __init__(
        self,
        modalidade_service: ModalidadeService,
        repositorio_matriculas: Repositorio,
    ):
        if not isinstance(modalidade_service, ModalidadeService):
            raise TypeError("O serviço de modalidade informado é inválido")

        if not isinstance(repositorio_matriculas, Repositorio):
            raise TypeError("O repositório de matrículas informado é inválido")

        if repositorio_matriculas.tipo != TipoRepositorio.MATRICULA:
            raise ValueError("O repositório informado não é de matrículas")

        self.__modalidade_service = modalidade_service
        self.__repositorio_matriculas = repositorio_matriculas

    def calcular_faturamento(
        self, cod_modalidade: int
    ) -> tuple[Modalidade, Professor, float]:
        if not isinstance(cod_modalidade, int):
            raise TypeError("O código informado é inválido")

        resultado = self.__modalidade_service.buscar(cod_modalidade)

        if resultado is None:
            raise ValueError("A modalidade informada não foi encontrada")

        modalidade, professor = resultado

        matriculas = self.__repositorio_matriculas.listar()

        total_aulas = 0

        for matricula in matriculas:
            if matricula["cod_modalidade"] == modalidade.codigo:
                total_aulas += matricula["qtde_aulas"]

        total_faturado = modalidade.valor_aula * total_aulas

        return modalidade, professor, total_faturado
