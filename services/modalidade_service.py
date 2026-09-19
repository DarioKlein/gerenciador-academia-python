from repositories import Repositorio, TipoRepositorio
from models import Modalidade


# Falta implementar as regras de negócio e validar o código de professor
class ModalidadeService:
    def __init__(self, repositorio_modalidades: Repositorio):
        if not isinstance(repositorio_modalidades, Repositorio):
            raise TypeError("O repositório informado é inválido")

        if repositorio_modalidades.tipo != TipoRepositorio.MODALIDADE:
            raise ValueError("O repositório informado não é de modalidades")

        self.__repositorio_modalidades = repositorio_modalidades

    def criar(self, modalidade: Modalidade) -> Modalidade:
        if not isinstance(modalidade, Modalidade):
            raise TypeError("A modalidade informada é inválida")

        self.__repositorio_modalidades.incluir(modalidade.para_dict())
        return modalidade

    def buscar(self, codigo: int) -> Modalidade | None:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro = self.__repositorio_modalidades.buscar(codigo)

        if registro is None:
            return None

        return Modalidade.dict_para_objeto(registro)

    def atualizar(self, codigo: int, modalidade_atualizada: Modalidade) -> Modalidade:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        if not isinstance(modalidade_atualizada, Modalidade):
            raise TypeError("A modalidade informada é inválida")

        self.__repositorio_modalidades.atualizar(
            codigo, modalidade_atualizada.para_dict()
        )

        return modalidade_atualizada

    def excluir(self, codigo: int) -> Modalidade:
        if not isinstance(codigo, int):
            raise TypeError("O código informado é inválido")

        registro_excluido = self.__repositorio_modalidades.excluir(codigo)

        return Modalidade.dict_para_objeto(registro_excluido)
