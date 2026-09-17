import json
from structures import ArvoreBinaria, No
from .tipo_repositorio import TipoRepositorio


class Repositorio:
    def __init__(self, tipo: TipoRepositorio):
        if not isinstance(tipo, TipoRepositorio):
            raise TypeError("O tipo do repositório é inválido")

        self.tipo = tipo
        self.caminho = f"data/{tipo.value}.txt"
        self.raiz: No | None = None

        with open(self.caminho, "a", encoding="utf-8"):
            pass

        self.reconstruir_indice()

    def reconstruir_indice(self) -> None:
        self.raiz = None
        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            while True:
                posicao = arquivo.tell()
                linha = arquivo.readline()

                if not linha:
                    break

                if linha.startswith("0|"):
                    continue

                dados = json.loads(linha[2:])
                codigo = dados["codigo"]
                self.raiz = ArvoreBinaria.incluir(self.raiz, codigo, posicao)

    def incluir(self, dados: dict):
        codigo = dados["codigo"]

        if ArvoreBinaria.buscar(self.raiz, codigo) is not None:
            raise ValueError("Já existe um registro com este código")

        linha = json.dumps(dados, ensure_ascii=False)

        with open(self.caminho, "a", encoding="utf-8") as arquivo:
            posicao = arquivo.tell()
            arquivo.write(f"1|{linha}\n")

        self.raiz = ArvoreBinaria.incluir(self.raiz, codigo, posicao)

    def buscar(self, codigo: int):
        no = ArvoreBinaria.buscar(self.raiz, codigo)

        if no is None:
            raise ValueError("O código para busca não foi encontrado")

        with open(self.caminho, "r", encoding="utf-8") as arquivo:
            arquivo.seek(no.posicao)
            linha = arquivo.readline()
            dado = json.loads(linha[2:])

        return dado

    def excluir(self, codigo: int):
        no = ArvoreBinaria.buscar(self.raiz, codigo)
        if no is None:
            raise ValueError("O código para exclusão não foi encontrado")

        with open(self.caminho, "r+", encoding="utf-8") as arquivo:
            arquivo.seek(no.posicao)
            arquivo.write("0")

        self.raiz = ArvoreBinaria.excluir(self.raiz, codigo)

        return True

    def atualizar(self, codigo, novos_dados: dict):
        no = ArvoreBinaria.buscar(self.raiz, codigo)

        if no is None:
            raise ValueError("O registro passado para atualização não existe")

        if novos_dados["codigo"] != codigo:
            raise ValueError("O código do registro não pode ser alterado")

        linha = json.dumps(novos_dados, ensure_ascii=False)

        with open(self.caminho, "r+", encoding="utf-8") as arquivo:
            arquivo.seek(0, 2)
            nova_posicao = arquivo.tell()
            arquivo.write(f"1|{linha}\n")
            arquivo.flush()

            arquivo.seek(no.posicao)
            arquivo.write("0")
        no.posicao = nova_posicao

        return True
