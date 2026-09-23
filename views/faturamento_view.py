import customtkinter as ctk

from models import Modalidade, Professor
from services import FaturamentoService
from utils import Conversor, Formatador


class FaturamentoView(ctk.CTkFrame):
    def __init__(self, master, faturamento_service: FaturamentoService):
        super().__init__(master, fg_color="transparent")

        if not isinstance(faturamento_service, FaturamentoService):
            raise TypeError("O serviço de faturamento informado é inválido")

        self.__faturamento_service = faturamento_service

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.__criar_cabecalho()
        self.__criar_area_busca()
        self.__criar_area_resultado()
        self.__criar_area_feedback()

    def __criar_cabecalho(self) -> None:
        cabecalho = ctk.CTkFrame(self, fg_color="transparent")
        cabecalho.grid(
            row=0,
            column=0,
            padx=30,
            pady=(30, 10),
            sticky="ew",
        )
        cabecalho.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            cabecalho,
            text="Faturamento por Modalidade",
            font=ctk.CTkFont(size=26, weight="bold"),
            anchor="w",
        ).grid(row=0, column=0, sticky="ew")

    def __criar_area_busca(self) -> None:
        busca = ctk.CTkFrame(self)
        busca.grid(
            row=1,
            column=0,
            padx=30,
            pady=10,
            sticky="ew",
        )
        busca.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            busca,
            text="Código da Modalidade",
        ).grid(
            row=0,
            column=0,
            padx=(20, 10),
            pady=20,
            sticky="w",
        )

        self.__campo_codigo = ctk.CTkEntry(busca, placeholder_text="Ex.: 1", height=38)
        self.__campo_codigo.grid(
            row=0,
            column=1,
            padx=10,
            pady=20,
            sticky="ew",
        )
        self.__campo_codigo.bind(
            "<Return>",
            lambda _evento: self.__calcular(),
        )

        ctk.CTkButton(
            busca, text="Calcular", command=self.__calcular, width=110, height=38
        ).grid(
            row=0,
            column=2,
            padx=(10, 20),
            pady=20,
        )

        self.__campo_codigo.focus()

    def __criar_area_resultado(self) -> None:
        self.__area_resultado = ctk.CTkFrame(
            self,
            fg_color="transparent",
        )
        self.__area_resultado.grid(
            row=2,
            column=0,
            padx=30,
            pady=10,
            sticky="nsew",
        )
        self.__area_resultado.grid_columnconfigure(0, weight=1)

    def __criar_area_feedback(self) -> None:
        self.__feedback = ctk.CTkLabel(
            self,
            text="",
            anchor="w",
            wraplength=700,
        )
        self.__feedback.grid(
            row=3,
            column=0,
            padx=35,
            pady=(5, 25),
            sticky="ew",
        )

    def __calcular(self) -> None:
        try:
            codigo = Conversor.para_inteiro(
                self.__campo_codigo.get(),
                "o código da modalidade",
            )

            modalidade, professor, total_faturado = (
                self.__faturamento_service.calcular_faturamento(codigo)
            )

            self.__limpar_resultado()
            self.__mostrar_resultado(
                modalidade,
                professor,
                total_faturado,
            )
            self.__mostrar_feedback(
                "Faturamento calculado com sucesso.",
                sucesso=True,
            )
        except (TypeError, ValueError, OSError) as erro:
            self.__limpar_resultado()
            self.__mostrar_feedback(
                str(erro),
                sucesso=False,
            )

    def __mostrar_resultado(
        self,
        modalidade: Modalidade,
        professor: Professor,
        total_faturado: float,
    ) -> None:
        cartao = ctk.CTkFrame(self.__area_resultado)
        cartao.grid(row=0, column=0, sticky="ew")
        cartao.grid_columnconfigure(1, weight=1)

        dados = (
            ("Código", str(modalidade.codigo)),
            ("Modalidade", modalidade.descricao),
            ("Professor", professor.nome),
            ("Valor da Aula", Formatador.moeda(modalidade.valor_aula)),
            ("Faturamento", Formatador.moeda(total_faturado)),
        )

        for linha, (rotulo, valor) in enumerate(dados):
            ctk.CTkLabel(
                cartao,
                text=f"{rotulo}:",
                font=ctk.CTkFont(weight="bold"),
                anchor="w",
            ).grid(
                row=linha,
                column=0,
                padx=(20, 10),
                pady=8,
                sticky="w",
            )

            ctk.CTkLabel(
                cartao,
                text=valor,
                anchor="w",
            ).grid(
                row=linha,
                column=1,
                padx=(10, 20),
                pady=8,
                sticky="ew",
            )

    def __limpar_resultado(self) -> None:
        for componente in self.__area_resultado.winfo_children():
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

        self.__feedback.configure(
            text=mensagem,
            text_color=cor,
        )
