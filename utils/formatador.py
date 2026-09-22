class Formatador:
    @staticmethod
    def telefone(telefone: str) -> str:
        return f"({telefone[:2]}) {telefone[2:7]}-{telefone[7:]}"

    @staticmethod
    def moeda(valor: float) -> str:
        return f"R$ {valor:.2f}".replace(".", ",")

    @staticmethod
    def decimal(valor: float, casas: int = 2) -> str:
        return f"{valor:.{casas}f}".replace(".", ",")
