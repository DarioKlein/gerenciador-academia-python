class Validador:
    @staticmethod
    def texto_e_valido(texto: str):
        return (
            bool(texto.strip())
            and any(caractere.isalpha() for caractere in texto)
            and all(
                caractere.isalpha() or caractere.isspace() or caractere == "'"
                for caractere in texto
            )
        )
