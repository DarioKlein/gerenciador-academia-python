class No:
    def __init__(
        self,
        codigo: int,
        posicao: int,
        esquerda: "No | None" = None,
        direita: "No | None" = None,
    ):
        self.codigo = codigo
        self.posicao = posicao
        self.esquerda = esquerda
        self.direita = direita
