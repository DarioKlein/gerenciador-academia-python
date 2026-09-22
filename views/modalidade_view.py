from tkinter import messagebox

import customtkinter as ctk

from models import Modalidade, Professor
from services import ModalidadeService
from utils import Formatador, Conversor


class ModalidadeView(ctk.CTkFrame):
    OPERACOES = ("Incluir", "Buscar", "Atualizar", "Excluir")

    def __init__(self, master, modalidade_service: ModalidadeService):
        super().__init__(master, fg_color="transparent")

        if not isinstance(modalidade_service, ModalidadeService):
            raise TypeError("O serviço de modalidades informado é inválido")

        self.__modalidade_service = modalidade_service
        self.__modalidade_selecionada: Modalidade | None = None
        self.__campos_formulario: dict[str, ctk.CTkEntry] = {}
        self.__campo_busca: ctk.CTkEntry | None = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.__criar_cabecalho()
        self.__criar_area_conteudo()
        self.__criar_area_feedback()
        self.__selecionar_operacao("Incluir")

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
        )
        self.__seletor_operacao.grid(
            row=1, column=0, padx=30, pady=(5, 10), sticky="ew"
        )
        self.__seletor_operacao.set("Incluir")

    def __criar_area_conteudo(self) -> None:
        self.__conteudo = ctk.CTkFrame(self)
        self.__conteudo.grid(row=2, column=0, padx=30, pady=10, sticky="nsew")
        self.__conteudo.grid_columnconfigure(0, weight=1)

    def __criar_area_feedback(self) -> None:
        self.__feedback = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            wraplength=700,
        )
        self.__feedback.grid(row=3, column=0, padx=35, pady=(5, 25), sticky="ew")

    def __selecionar_operacao(self, operacao: str) -> None:
        self.__modalidade_selecionada = None
        self.__campos_formulario = {}
        self.__campo_busca = None
        self.__limpar_conteudo()
        self.__mostrar_feedback("")
        self.__titulo.configure(text=f"Gerenciamento de Modalidades — {operacao}")

        acoes = {
            "Incluir": self.__montar_inclusao,
            "Buscar": self.__montar_busca,
            "Atualizar": self.__montar_atualizacao,
            "Excluir": self.__montar_exclusao,
        }
        acoes[operacao]()

    def __montar_inclusao(self) -> None:
        self.__criar_formulario(self.__conteudo)

        ctk.CTkButton(
            self.__conteudo,
            text="Salvar Modalidade",
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

        ctk.CTkLabel(busca, text="Código da Modalidade").grid(
            row=0, column=0, padx=(0, 10), sticky="w"
        )

        self.__campo_busca = ctk.CTkEntry(busca, placeholder_text="Ex.: 1")
        self.__campo_busca.grid(row=0, column=1, padx=10, sticky="ew")
        self.__campo_busca.bind("<Return>", lambda _evento: comando())

        ctk.CTkButton(busca, text="Buscar", command=comando, width=110).grid(
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

    def __criar_formulario(self, master, modalidade: Modalidade | None = None) -> None:
        formulario = ctk.CTkFrame(master, fg_color="transparent")
        formulario.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        formulario.grid_columnconfigure(1, weight=1)

        campos = (
            ("codigo", "Código", "Ex.: 1"),
            ("descricao", "Descrição", "Ex.: Musculação"),
            ("cod_prof", "Código do Professor", "Ex.: 1"),
            ("valor_aula", "Valor da Aula", "Ex.: 150,00"),
            ("limite_alunos", "Limite Total de Alunos", "Ex.: 40"),
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

            campo = ctk.CTkEntry(formulario, placeholder_text=placeholder)
            campo.grid(row=linha, column=1, pady=8, sticky="ew")
            self.__campos_formulario[chave] = campo

        self.__rotulo_professor = ctk.CTkLabel(
            formulario,
            text="",
            anchor="w",
        )
        self.__rotulo_professor.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(25, 0),
            sticky="w",
        )

        campo_professor = self.__campos_formulario["cod_prof"]
        campo_professor.bind("<Return>", self.__mostrar_professor_selecionado)
        campo_professor.bind("<FocusOut>", self.__mostrar_professor_selecionado)

        if modalidade is not None:
            self.__preencher_formulario(modalidade)
            self.__campos_formulario["codigo"].configure(state="disabled")

            self.__mostrar_professor_selecionado()
        else:
            self.__campos_formulario["codigo"].focus()

    def __mostrar_professor_selecionado(self, _evento=None) -> None:
        texto = self.__campos_formulario["cod_prof"].get().strip()

        if not texto:
            self.__rotulo_professor.configure(text="")
            return

        try:
            codigo = Conversor.para_inteiro(texto, "o código do professor")
            professor = self.__modalidade_service.buscar_professor(codigo)

            if professor is None:
                self.__rotulo_professor.configure(
                    text="Professor não encontrado",
                    text_color=("#991b1b", "#f87171"),
                )
                return

            self.__rotulo_professor.configure(
                text=f"Professor encontrado: {professor.nome}",
                text_color=("gray20", "gray80"),
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__rotulo_professor.configure(
                text=str(erro),
                text_color=("#991b1b", "#f87171"),
            )

    def __preencher_formulario(self, modalidade: Modalidade) -> None:
        valores = {
            "codigo": str(modalidade.codigo),
            "descricao": str(modalidade.descricao),
            "cod_prof": str(modalidade.cod_prof),
            "valor_aula": Formatador.decimal(modalidade.valor_aula),
            "limite_alunos": str(modalidade.limite_alunos),
        }

        for chave, valor in valores.items():
            campo = self.__campos_formulario[chave]
            campo.insert(0, valor)

    def __obter_modalidade_formulario(self) -> Modalidade:
        codigo = Conversor.para_inteiro(
            self.__campos_formulario["codigo"].get(), "o código da modalidade"
        )
        descricao = self.__campos_formulario["descricao"].get().strip()
        cod_prof = Conversor.para_inteiro(
            self.__campos_formulario["cod_prof"].get(), "o código do professor"
        )
        valor_aula = Conversor.para_decimal(
            self.__campos_formulario["valor_aula"].get(), "o valor da aula"
        )
        limite_alunos = Conversor.para_inteiro(
            self.__campos_formulario["limite_alunos"].get(), "o limite de alunos"
        )

        if (
            self.__modalidade_selecionada is not None
            and limite_alunos < self.__modalidade_selecionada.total_alunos
        ):
            raise ValueError(
                "O limite de alunos não pode ser menor que o total atual de alunos"
            )

        total_alunos = 0

        if self.__modalidade_selecionada is not None:
            total_alunos = self.__modalidade_selecionada.total_alunos

        return Modalidade(
            codigo, descricao, cod_prof, valor_aula, limite_alunos, total_alunos
        )

    def __obter_codigo_busca(self) -> int:
        if self.__campo_busca is None:
            raise ValueError("O campo de busca não está disponível")

        return Conversor.para_inteiro(
            self.__campo_busca.get(), "o código da modalidade"
        )

    def __buscar_modalidade(self) -> tuple[Modalidade, Professor]:
        resultado = self.__modalidade_service.buscar(self.__obter_codigo_busca())

        if resultado is None:
            raise ValueError("A modalidade informada não foi encontrada")

        return resultado

    def __incluir(self) -> None:
        try:
            modalidade = self.__obter_modalidade_formulario()
            self.__modalidade_service.criar(modalidade)
            self.__limpar_formulario()
            self.__mostrar_feedback(
                f"Modalidade {modalidade.descricao} incluída com sucesso.", sucesso=True
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_exibir(self) -> None:
        try:
            modalidade, professor = self.__buscar_modalidade()
            self.__limpar_area_operacao()
            self.__mostrar_dados_modalidade(self.__area_operacao, modalidade, professor)
            self.__mostrar_feedback("Modalidade encontrada.", sucesso=True)
        except (TypeError, ValueError, OSError) as erro:
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_atualizar(self) -> None:
        try:
            modalidade, professor = self.__buscar_modalidade()
            self.__modalidade_selecionada = modalidade
            self.__limpar_area_operacao()
            self.__criar_formulario(self.__area_operacao, modalidade)

            ctk.CTkButton(
                self.__area_operacao,
                text="Atualizar modalidade",
                command=self.__atualizar,
                height=38,
            ).grid(row=1, column=0, padx=20, pady=(0, 10), sticky="e")

            self.__mostrar_feedback(
                "Modalidade encontrada. Altere os campos desejados.", sucesso=True
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__modalidade_selecionada = None
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __atualizar(self) -> None:
        try:
            if self.__modalidade_selecionada is None:
                raise ValueError("Busque uma modalidade antes de atualizá-la")

            modalidade_atualizada = self.__obter_modalidade_formulario()
            self.__modalidade_service.atualizar(
                self.__modalidade_selecionada.codigo,
                modalidade_atualizada,
            )
            self.__modalidade_selecionada = modalidade_atualizada
            self.__mostrar_feedback(
                f"Modalidade {modalidade_atualizada.descricao} atualizada com sucesso.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_excluir(self) -> None:
        try:
            modalidade, professor = self.__buscar_modalidade()
            self.__modalidade_selecionada = modalidade
            self.__limpar_area_operacao()
            self.__mostrar_dados_modalidade(self.__area_operacao, modalidade, professor)

            ctk.CTkButton(
                self.__area_operacao,
                text="Confirmar exclusão",
                command=self.__excluir,
                height=38,
                fg_color="#b91c1c",
                hover_color="#991b1b",
            ).grid(row=1, column=0, padx=20, pady=(15, 0), sticky="e")

            self.__mostrar_feedback(
                "Confira os dados antes de confirmar a exclusão.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__modalidade_selecionada = None
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __excluir(self) -> None:
        try:
            if self.__modalidade_selecionada is None:
                raise ValueError("Busque uma modalidade antes de excluí-la")

            if not messagebox.askyesno(
                "Confirmar exclusão",
                f"Deseja excluir a modalidade {self.__modalidade_selecionada.descricao}?",
                parent=self.winfo_toplevel(),
            ):
                return

            modalidade_excluida = self.__modalidade_service.excluir(
                self.__modalidade_selecionada.codigo
            )
            self.__modalidade_selecionada = None
            self.__limpar_area_operacao()
            self.__limpar_campo_busca()
            self.__mostrar_feedback(
                f"Modalidade {modalidade_excluida.descricao} excluída com sucesso.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    @staticmethod
    def __mostrar_dados_modalidade(
        master, modalidade: Modalidade, professor: Professor
    ) -> None:
        cartao = ctk.CTkFrame(master)
        cartao.grid(row=0, column=0, sticky="ew")
        cartao.grid_columnconfigure(1, weight=1)

        dados = (
            ("Código", str(modalidade.codigo)),
            ("Descrição", modalidade.descricao),
            ("Código do Professor", modalidade.cod_prof),
            ("Nome do Professor", professor.nome),
            ("Valor da Aula", Formatador.moeda(modalidade.valor_aula)),
            ("Limite de Alunos", f"{modalidade.limite_alunos}"),
            ("Total de Alunos", f"{modalidade.total_alunos}"),
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

        self.__rotulo_professor.configure(text="")
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
