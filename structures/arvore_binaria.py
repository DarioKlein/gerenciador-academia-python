from .no import No


class ArvoreBinaria:
    @staticmethod
    def buscar(raiz: No, codigo: int) -> No | None:
        atual: No | None = raiz
        while atual is not None:
            if codigo == atual.codigo:
                return atual
            if codigo < atual.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita
        return None

    @staticmethod
    def incluir(raiz: No, codigo: int, posicao: int) -> No:
        novo: No = No(codigo, posicao, None, None)
        if raiz is None:
            return novo
        atual: No | None = raiz
        pai: No | None = None

        while atual is not None:
            pai = atual
            if codigo == atual.codigo:
                raise ValueError("Já existe um registro com este código")
            elif codigo < atual.codigo:
                atual = atual.esquerda
            else:
                atual = atual.direita

        if codigo < pai.codigo:
            pai.esquerda = novo
        else:
            pai.direita = novo
        return raiz

    @staticmethod
    def excluir(raiz: No, codigo: int) -> No | None:
        pass
