class Conversor:
    @staticmethod
    def para_inteiro(texto: str, nome_campo: str) -> int:
        texto = texto.strip()

        if not texto:
            raise ValueError(f"Informe {nome_campo}")

        try:
            return int(texto)
        except ValueError as erro:
            raise ValueError(
                f"{nome_campo.capitalize()} deve ser um número inteiro"
            ) from erro

    @staticmethod
    def para_decimal(texto: str, nome_campo: str) -> float:
        texto = texto.strip().replace(",", ".")

        if not texto:
            raise ValueError(f"Informe {nome_campo}")

        try:
            return float(texto)
        except ValueError as erro:
            raise ValueError(
                f"{nome_campo.capitalize()} deve ser um número válido"
            ) from erro
