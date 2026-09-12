import json
from structures import ArvoreBinaria, No


class Persistencia:
    def __init__(self, caminho: str):
        self.caminho = caminho
        self.raiz: No | None = None

        with open(self.caminho, "ab"):
            pass

    def reconstruir_indice(self):
        pass

    def incluir(self):
        pass

    def buscar(self):
        pass

    def excluir(self):
        pass

    def atualizar(self):
        pass
