class ValidadorTexto:
    @staticmethod
    def eh_valido(texto):
        return all(c.isalpha() or c.isspace() for c in texto)
