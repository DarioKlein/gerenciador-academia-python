from tkinter import messagebox

import customtkinter as ctk

from models import Matricula, Aluno, Modalidade
from services import MatriculaService
from utils import Conversor


class MatriculaView(ctk.CTkFrame):
    OPERACOES = ("Incluir", "Buscar", "Atualizar", "Excluir")

    def __init__(self, master, matricula_service: MatriculaService):
        super().__init__(master, fg_color="transparent")

        if not isinstance(matricula_service, MatriculaService):
            raise TypeError("O serviço de matrículas informado é inválido")

        self.__matricula_service = matricula_service
        self.__matricula_selecionada: Matricula | None = None
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
            height=38,
            text_color="#fff",
            selected_color="#1a1919",
            selected_hover_color="#1a1919",
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
        self.__matricula_selecionada = None
        self.__campos_formulario = {}
        self.__campo_busca = None
        self.__limpar_conteudo()
        self.__mostrar_feedback("")
        self.__titulo.configure(text=f"Gerenciamento de Matrículas — {operacao}")

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
            text="Salvar Matrícula",
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

        ctk.CTkLabel(busca, text="Código da Matrícula").grid(
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

    def __criar_formulario(self, master, matricula: Matricula | None = None) -> None:
        formulario = ctk.CTkFrame(master, fg_color="transparent")
        formulario.grid(row=0, column=0, padx=20, pady=20, sticky="ew")
        formulario.grid_columnconfigure(1, weight=1)

        campos = (
            ("codigo", "Código", "Ex.: 1"),
            ("cod_aluno", "Código do Aluno", "Ex.: 1"),
            ("cod_modalidade", "Código da Modalidade", "Ex.: 1"),
            ("qtde_aulas", "Quantidade de Aulas", "Ex.: 4"),
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

        self.__rotulo_aluno = ctk.CTkLabel(
            formulario,
            text="",
            anchor="w",
        )
        self.__rotulo_aluno.grid(
            row=4,
            column=0,
            columnspan=2,
            pady=(25, 0),
            sticky="w",
        )

        self.__rotulo_modalidade = ctk.CTkLabel(
            formulario,
            text="",
            anchor="w",
        )
        self.__rotulo_modalidade.grid(
            row=5,
            column=0,
            columnspan=2,
            pady=(3, 0),
            sticky="w",
        )

        campo_aluno = self.__campos_formulario["cod_aluno"]
        campo_aluno.bind("<Return>", self.__mostrar_aluno_selecionado)
        campo_aluno.bind("<FocusOut>", self.__mostrar_aluno_selecionado)

        campo_modalidade = self.__campos_formulario["cod_modalidade"]
        campo_modalidade.bind("<Return>", self.__mostrar_modalidade_selecionada)
        campo_modalidade.bind("<FocusOut>", self.__mostrar_modalidade_selecionada)

        if matricula is not None:
            self.__preencher_formulario(matricula)
            self.__campos_formulario["codigo"].configure(state="disabled")
            self.__campos_formulario["cod_aluno"].configure(state="disabled")

            self.__mostrar_aluno_selecionado()
            self.__mostrar_modalidade_selecionada()
        else:
            self.__campos_formulario["codigo"].focus()

    def __mostrar_aluno_selecionado(self, _evento=None) -> None:
        texto = self.__campos_formulario["cod_aluno"].get().strip()

        if not texto:
            self.__rotulo_aluno.configure(text="")
            return

        try:
            codigo = Conversor.para_inteiro(texto, "o código do aluno")
            aluno = self.__matricula_service.buscar_aluno(codigo)

            if aluno is None:
                self.__rotulo_aluno.configure(
                    text="Aluno não encontrado",
                    text_color=("#991b1b", "#f87171"),
                )
                return

            self.__rotulo_aluno.configure(
                text=f"Aluno encontrado: {aluno.nome}",
                text_color=("gray20", "gray80"),
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__rotulo_aluno.configure(
                text=str(erro),
                text_color=("#991b1b", "#f87171"),
            )

    def __mostrar_modalidade_selecionada(self, _evento=None) -> None:
        texto = self.__campos_formulario["cod_modalidade"].get().strip()

        if not texto:
            self.__rotulo_modalidade.configure(text="")
            return

        try:
            codigo = Conversor.para_inteiro(
                texto,
                "o código da modalidade",
            )
            modalidade = self.__matricula_service.buscar_modalidade(codigo)

            if modalidade is None:
                self.__rotulo_modalidade.configure(
                    text="Modalidade não encontrada",
                    text_color=("#991b1b", "#f87171"),
                )
                return

            self.__rotulo_modalidade.configure(
                text=f"Modalidade encontrada: {modalidade.descricao}",
                text_color=("gray20", "gray80"),
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__rotulo_modalidade.configure(
                text=str(erro),
                text_color=("#991b1b", "#f87171"),
            )

    def __preencher_formulario(self, matricula: Matricula) -> None:
        valores = {
            "codigo": str(matricula.codigo),
            "cod_aluno": str(matricula.cod_aluno),
            "cod_modalidade": str(matricula.cod_modalidade),
            "qtde_aulas": str(matricula.qtde_aulas),
        }

        for chave, valor in valores.items():
            campo = self.__campos_formulario[chave]
            campo.insert(0, valor)

    def __obter_matricula_formulario(self) -> Matricula:
        codigo = Conversor.para_inteiro(
            self.__campos_formulario["codigo"].get(), "o código da matrícula"
        )
        cod_aluno = Conversor.para_inteiro(
            self.__campos_formulario["cod_aluno"].get(), "o código do aluno"
        )
        cod_modalidade = Conversor.para_inteiro(
            self.__campos_formulario["cod_modalidade"].get(), "o código da modalidade"
        )
        qtde_aulas = Conversor.para_inteiro(
            self.__campos_formulario["qtde_aulas"].get(), "a quantidade de aulas"
        )

        return Matricula(codigo, cod_aluno, cod_modalidade, qtde_aulas)

    def __obter_codigo_busca(self) -> int:
        if self.__campo_busca is None:
            raise ValueError("O campo de busca não está disponível")

        return Conversor.para_inteiro(self.__campo_busca.get(), "o código da matrícula")

    def __buscar_matricula(self) -> tuple[Matricula, Aluno, Modalidade]:
        resultado = self.__matricula_service.buscar(self.__obter_codigo_busca())

        if resultado is None:
            raise ValueError("A matrícula informada não foi encontrada")

        return resultado

    def __incluir(self) -> None:
        try:
            matricula = self.__obter_matricula_formulario()
            self.__matricula_service.criar(matricula)
            self.__limpar_formulario()
            self.__mostrar_feedback(
                f"Matrícula {matricula.codigo} incluída com sucesso.", sucesso=True
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_exibir(self) -> None:
        try:
            matricula, aluno, modalidade = self.__buscar_matricula()
            self.__limpar_area_operacao()
            self.__mostrar_dados_matricula(
                self.__area_operacao, matricula, aluno, modalidade
            )
            self.__mostrar_feedback("Matrícula encontrada.", sucesso=True)
        except (TypeError, ValueError, OSError) as erro:
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_atualizar(self) -> None:
        try:
            matricula, aluno, modalidade = self.__buscar_matricula()
            self.__matricula_selecionada = matricula
            self.__limpar_area_operacao()
            self.__criar_formulario(self.__area_operacao, matricula)

            ctk.CTkButton(
                self.__area_operacao,
                text="Atualizar matrícula",
                command=self.__atualizar,
                height=38,
            ).grid(row=1, column=0, padx=20, pady=(0, 10), sticky="e")

            self.__mostrar_feedback(
                "Matrícula encontrada. Altere os campos desejados.", sucesso=True
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__matricula_selecionada = None
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __atualizar(self) -> None:
        try:
            if self.__matricula_selecionada is None:
                raise ValueError("Busque uma matrícula antes de atualizá-la")

            matricula_atualizada = self.__obter_matricula_formulario()
            self.__matricula_service.atualizar(
                self.__matricula_selecionada.codigo,
                matricula_atualizada,
            )
            self.__matricula_selecionada = matricula_atualizada
            self.__mostrar_feedback(
                f"Matrícula {matricula_atualizada.codigo} atualizada com sucesso.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __buscar_para_excluir(self) -> None:
        try:
            matricula, aluno, modalidade = self.__buscar_matricula()
            self.__matricula_selecionada = matricula
            self.__limpar_area_operacao()
            self.__mostrar_dados_matricula(
                self.__area_operacao, matricula, aluno, modalidade
            )

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
            self.__matricula_selecionada = None
            self.__limpar_area_operacao()
            self.__mostrar_feedback(str(erro), sucesso=False)

    def __excluir(self) -> None:
        try:
            if self.__matricula_selecionada is None:
                raise ValueError("Busque uma matrícula antes de excluí-la")

            if not messagebox.askyesno(
                "Confirmar exclusão",
                f"Deseja excluir a matrícula {self.__matricula_selecionada.codigo}?",
                parent=self.winfo_toplevel(),
            ):
                return

            matricula_excluida = self.__matricula_service.excluir(
                self.__matricula_selecionada.codigo
            )
            self.__matricula_selecionada = None
            self.__limpar_area_operacao()
            self.__limpar_campo_busca()
            self.__mostrar_feedback(
                f"Matrícula {matricula_excluida.codigo} excluída com sucesso.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__mostrar_feedback(str(erro), sucesso=False)

    @staticmethod
    def __mostrar_dados_matricula(
        master, matricula: Matricula, aluno: Aluno, modalidade: Modalidade
    ) -> None:
        cartao = ctk.CTkFrame(master)
        cartao.grid(row=0, column=0, sticky="ew")
        cartao.grid_columnconfigure(1, weight=1)

        dados = (
            ("Código", str(matricula.codigo)),
            ("Código do Aluno", str(matricula.cod_aluno)),
            ("Nome do Aluno", aluno.nome),
            ("Código da Modalidade", str(matricula.cod_modalidade)),
            ("Descrição da Modalidade", modalidade.descricao),
            ("Quantidade de Aulas", str(matricula.qtde_aulas)),
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

        self.__rotulo_aluno.configure(text="")
        self.__rotulo_modalidade.configure(text="")
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
