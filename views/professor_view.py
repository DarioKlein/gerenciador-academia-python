from tkinter import messagebox

import customtkinter as ctk

from models import Professor
from services import ProfessorService
from utils import Conversor, Formatador


class ProfessorView(ctk.CTkFrame):
    OPERACOES = ("Listar", "Incluir", "Buscar", "Atualizar", "Excluir")

    def __init__(self, master, professor_service: ProfessorService):
        super().__init__(master, fg_color="transparent")

        if not isinstance(professor_service, ProfessorService):
            raise TypeError("O serviço de professores informado é inválido")

        self.__professor_service = professor_service
        self.__professor_selecionado: Professor | None = None
        self.__campos_formulario: dict[str, ctk.CTkEntry] = {}
        self.__campo_busca: ctk.CTkEntry | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.__criar_cabecalho()
        self.__criar_area_conteudo()
        self.__criar_area_feedback()
        self.__selecionar_operacao("Listar")

    def __criar_cabecalho(self) -> None:
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.grid(row=0, column=0, padx=30, pady=(30, 10), sticky="ew")
        cabecalho.grid_columnconfigure(0, weight=1)

        self.__titulo = ctk.CTkLabel(
            cabecalho,
            text="",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        )
        self.__titulo.grid(row=0, column=0, sticky="ew")

        self.__seletor_operacao = ctk.CTkSegmentedButton(
            self,
            values=list(self.OPERACOES),
            command=self.__selecionar_operacao,
            height=38,
            text_color="#fff",
            selected_color="#1a1919",
            selected_hover_color="#1a1919",
        )
        self.__seletor_operacao.grid(
            row=1, column=0, padx=30, pady=(5, 10), sticky="ew"
        )
        self.__seletor_operacao.set("Listar")

    def __criar_area_conteudo(self) -> None:
        self.__conteudo = ctk.CTkFrame(self)
        self.__conteudo.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        self.__conteudo.grid_columnconfigure(0, weight=1)

    def __criar_area_feedback(self) -> None:
        self.__feedback = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            justify="left",
            wraplength=700,
        )
        self.__feedback.grid(row=3, column=0, padx=35, pady=(5, 25), sticky="ew")

    def __selecionar_operacao(self, operacao: str) -> None:
        self.__professor_selecionado = None
        self.__campos_formulario = {}
        self.__campo_busca = None

        self.__conteudo.grid_rowconfigure(0, weight=0)

        self.__limpar_conteudo()
        self.__mostrar_feedback("")
        self.__titulo.configure(text=f"Gerenciamento de Professores — {operacao}")

        acoes = {
            "Listar": self.__montar_listagem,
            "Incluir": self.__montar_inclusao,
            "Buscar": self.__montar_busca,
            "Atualizar": self.__montar_atualizacao,
            "Excluir": self.__montar_exclusao,
        }
        acoes[operacao]()

    def __montar_listagem(self) -> None:
        professores = self.__professor_service.listar()

        if not professores:
            ctk.CTkLabel(
                self.__conteudo,
                text="Nenhum professor cadastrado no momento.",
                font=ctk.CTkFont(size=16),
                text_color="#fff",
            ).grid(row=0, column=0, padx=20, pady=30)
            return

        tabela = ctk.CTkScrollableFrame(self.__conteudo, height=450)
        tabela.grid(row=0, column=0, padx=0, pady=0, sticky="nsew")
        self.__conteudo.grid_rowconfigure(0, weight=1)

        colunas = (
            "Código",
            "Nome",
            "Endereço",
            "Telefone",
        )
        for col_idx, rotulo in enumerate(colunas):
            tabela.grid_columnconfigure(col_idx, weight=1)
            ctk.CTkLabel(
                tabela, text=rotulo, font=ctk.CTkFont(weight="bold"), anchor="center"
            ).grid(row=0, column=col_idx, padx=10, pady=8, sticky="ew")

        for linha_idx, professor in enumerate(professores, start=1):
            valores = (
                str(professor.codigo),
                professor.nome,
                professor.endereco,
                Formatador.telefone(professor.telefone),
            )
            for col_idx, valor in enumerate(valores):
                ctk.CTkLabel(tabela, text=valor, anchor="center").grid(
                    row=linha_idx, column=col_idx, padx=10, pady=6, sticky="ew"
                )

    def __montar_inclusao(self) -> None:
        self.__criar_formulario(self.__conteudo)

        ctk.CTkButton(
            self.__conteudo,
            text="Salvar Professor",
            command=self.__incluir,
            height=38,
        ).grid(row=1, column=0, padx=20, pady=(10, 20), sticky="e")

    def __montar_busca(self) -> None:
        self.__criar_barra_busca(self.__buscar_para_exibir)
        self.__criar_area_operacao()

    def __montar_atualizacao(self) -> None:
        self.__criar_barra_busca(self.__buscar_para_atualizar)
        self.__criar_area_operacao()

    def __montar_exclusao(self) -> None:
        self.__criar_barra_busca(self.__buscar_para_excluir)
        self.__criar_area_operacao()

    def __criar_barra_busca(self, comando) -> None:
        busca = ctk.CTkFrame(self.__conteudo, fg_color="transparent")
        busca.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        busca.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(busca, text="Código do Professor").grid(
            row=0, column=0, padx=(0, 10), sticky="w"
        )

        self.__campo_busca = ctk.CTkEntry(busca, placeholder_text="Ex.: 1", height=38)
        self.__campo_busca.grid(row=0, column=1, padx=10, sticky="ew")
        self.__campo_busca.bind("<Return>", lambda _evento: comando())

        ctk.CTkButton(busca, text="Buscar", command=comando, width=110, height=38).grid(
            row=0, column=2, padx=(10, 0)
        )
        self.__campo_busca.focus()

    def __criar_area_operacao(self) -> None:
        self.__area_operacao = ctk.CTkFrame(
            self.__conteudo,
            fg_color="transparent",
        )
        self.__area_operacao.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="ew")
        self.__area_operacao.grid_columnconfigure(0, weight=1)

    def __criar_formulario(self, master, professor: Professor | None = None) -> None:
        formulario = ctk.CTkFrame(master, fg_color="transparent")
        formulario.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        formulario.grid_columnconfigure(1, weight=1)

        campos = (
            ("codigo", "Código", "Ex.: 1"),
            ("nome", "Nome", "Ex.: Maria da Silva"),
            ("endereco", "Endereço", "Ex.: Rua Nagib Elias 279"),
            ("telefone", "Telefone", "Ex.: 18997809007"),
        )

        self.__campos_formulario = {}

        for linha, (chave, texto, placeholder) in enumerate(campos):
            ctk.CTkLabel(formulario, text=texto, anchor="w").grid(
                row=linha,
                column=0,
                padx=(0, 15),
                pady=8,
                sticky="w",
            )

            campo = ctk.CTkEntry(formulario, placeholder_text=placeholder, height=38)
            campo.grid(row=linha, column=1, pady=8, sticky="ew")
            self.__campos_formulario[chave] = campo

        if professor is not None:
            self.__preencher_formulario(professor)
            self.__campos_formulario["codigo"].configure(state="disabled")
        else:
            self.__campos_formulario["codigo"].focus()

    def __preencher_formulario(self, professor: Professor) -> None:
        valores = {
            "codigo": str(professor.codigo),
            "nome": str(professor.nome),
            "endereco": str(professor.endereco),
            "telefone": str(professor.telefone),
        }

        for chave, valor in valores.items():
            campo = self.__campos_formulario[chave]
            campo.insert(0, valor)

    def __obter_professor_formulario(self) -> Professor:
        codigo = Conversor.para_inteiro(
            self.__campos_formulario["codigo"].get(), "o código do professor"
        )
        nome = self.__campos_formulario["nome"].get().strip()
        endereco = self.__campos_formulario["endereco"].get().strip()
        telefone = self.__campos_formulario["telefone"].get().strip()

        return Professor(codigo, nome, endereco, telefone)

    def __obter_codigo_busca(self) -> int:
        if self.__campo_busca is None:
            raise ValueError("O campo de busca não está disponível")

        return Conversor.para_inteiro(self.__campo_busca.get(), "o código do professor")

    def __buscar_professor(self) -> Professor:
        professor = self.__professor_service.buscar(self.__obter_codigo_busca())

        if professor is None:
            raise ValueError("O professor informado não foi encontrado")

        return professor

    def __incluir(self) -> None:
        try:
            professor = self.__obter_professor_formulario()
            self.__professor_service.criar(professor)
            self.__limpar_formulario()
            self.__mostrar_feedback(
                f"Professor {professor.nome} incluído com sucesso.", sucesso=True
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_exibir(self) -> None:
        try:
            professor = self.__buscar_professor()
            self.__limpar_area_operacao()
            self.__mostrar_dados_professor(self.__area_operacao, professor)
            self.__mostrar_feedback("Professor encontrado.", sucesso=True)
        except (TypeError, ValueError, OSError) as erro:
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_atualizar(self) -> None:
        try:
            professor = self.__buscar_professor()
            self.__professor_selecionado = professor
            self.__limpar_area_operacao()
            self.__criar_formulario(self.__area_operacao, professor)

            ctk.CTkButton(
                self.__area_operacao,
                text="Atualizar professor",
                command=self.__atualizar,
                height=38,
            ).grid(row=1, column=0, padx=20, pady=(0, 10), sticky="e")

            self.__mostrar_feedback(
                "Professor encontrado. Altere os campos desejados.", sucesso=True
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__professor_selecionado = None
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __atualizar(self) -> None:
        try:
            if self.__professor_selecionado is None:
                raise ValueError("Busque um professor antes de atualizá-lo")

            professor_atualizado = self.__obter_professor_formulario()
            self.__professor_service.atualizar(
                self.__professor_selecionado.codigo,
                professor_atualizado,
            )
            self.__professor_selecionado = professor_atualizado
            self.__mostrar_feedback(
                f"Professor {professor_atualizado.nome} atualizado com sucesso.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_excluir(self) -> None:
        try:
            professor = self.__buscar_professor()
            self.__professor_selecionado = professor
            self.__limpar_area_operacao()
            self.__mostrar_dados_professor(self.__area_operacao, professor)

            ctk.CTkButton(
                self.__area_operacao,
                text="     Confirmar exclusão     ",
                command=self.__excluir,
                height=38,
                fg_color="#b91c1c",
                hover_color="#991b1b",
                text_color="#fff",
            ).grid(row=1, column=0, padx=20, pady=(15, 0), sticky="e")

            self.__mostrar_feedback(
                "Confira os dados antes de confirmar a exclusão.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__professor_selecionado = None
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __excluir(self) -> None:
        try:
            if self.__professor_selecionado is None:
                raise ValueError("Busque um professor antes de excluí-lo")

            if not messagebox.askyesno(
                "Confirmar exclusão",
                f"Deseja excluir o professor {self.__professor_selecionado.nome}?",
                parent=self.winfo_toplevel(),
            ):
                return

            professor_excluido = self.__professor_service.excluir(
                self.__professor_selecionado.codigo
            )
            self.__professor_selecionado = None
            self.__limpar_area_operacao()
            self.__limpar_campo_busca()
            self.__mostrar_feedback(
                f"Professor {professor_excluido.nome} excluído com sucesso.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    @staticmethod
    def __mostrar_dados_professor(master, professor: Professor) -> None:
        cartao = ctk.CTkFrame(master)
        cartao.grid(row=0, column=0, sticky="ew")
        cartao.grid_columnconfigure(1, weight=1)

        dados = (
            ("Código", str(professor.codigo)),
            ("Nome", professor.nome),
            ("Endereço", professor.endereco),
            ("Telefone", Formatador.telefone(professor.telefone)),
        )

        for linha, (rotulo, valor) in enumerate(dados):
            ctk.CTkLabel(
                cartao,
                text=f"{rotulo}:",
                font=ctk.CTkFont(weight="bold"),
                anchor="w",
            ).grid(row=linha, column=0, padx=(20, 10), pady=7, sticky="w")

            ctk.CTkLabel(cartao, text=valor, anchor="w").grid(
                row=linha,
                column=1,
                padx=(10, 20),
                pady=7,
                sticky="ew",
            )

    def __limpar_formulario(self) -> None:
        for campo in self.__campos_formulario.values():
            campo.delete(0, "end")

        self.__campos_formulario["codigo"].focus()

    def __limpar_campo_busca(self) -> None:
        if self.__campo_busca is not None:
            self.__campo_busca.delete(0, "end")
            self.__campo_busca.focus()

    def __limpar_conteudo(self) -> None:
        for componente in self.__conteudo.winfo_children():
            componente.destroy()

    def __limpar_area_operacao(self) -> None:
        for componente in self.__area_operacao.winfo_children():
            componente.destroy()

    def __mostrar_feedback(
        self,
        mensagem: str,
        sucesso: bool | None = None,
    ) -> None:
        if sucesso is True:
            cor = ("#166534", "#4ade80")
        elif sucesso is False:
            cor = ("#991b1b", "#f87171")
        else:
            cor = ("gray20", "gray80")

        self.__feedback.configure(text=mensagem, text_color=cor)
