class No:
    def __init__(
        self,
        codigo: int | None = None,
        posicao: int | None = None,
        esquerda: "No | None" = None,
        direita: "No | None" = None,
    ):
        self.codigo: int | None = codigo
        self.posicao: int | None = posicao
        self.esquerda: No | None = esquerda
        self.direita: No | None = direita
