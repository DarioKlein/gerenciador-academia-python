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
    def __menor(raiz: No) -> No | None:
        atual: No | None = raiz

        while atual.esquerda is not None:
            atual = atual.esquerda

        return atual

    @staticmethod
    def excluir(raiz: No, codigo: int) -> No | None:
        if raiz is None:
            return None

        if codigo < raiz.codigo:
            raiz.esquerda = ArvoreBinaria.excluir(raiz.esquerda, codigo)
        elif codigo > raiz.codigo:
            raiz.direita = ArvoreBinaria.excluir(raiz.direita, codigo)
        else:
            if raiz.esquerda is None and raiz.direita is None:
                return None
            elif raiz.esquerda is None:
                aux: No = raiz.direita
                return aux
            elif raiz.direita is None:
                aux: No = raiz.esquerda
                return aux
            else:
                aux: No = ArvoreBinaria.__menor(raiz.direita)
                raiz.codigo = aux.codigo
                raiz.posicao = aux.posicao
                raiz.direita = ArvoreBinaria.excluir(raiz.direita, aux.codigo)
        return raiz
