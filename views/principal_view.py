import customtkinter as ctk

from services import (
    AlunoService,
    ProfessorService,
    ModalidadeService,
    MatriculaService,
    FaturamentoService,
)
from .aluno_view import AlunoView
from .professor_view import ProfessorView
from .modalidade_view import ModalidadeView
from .matricula_view import MatriculaView
from .faturamento_view import FaturamentoView


class PrincipalView(ctk.CTkFrame):
    def __init__(
        self,
        master,
        aluno_service: AlunoService,
        professor_service: ProfessorService,
        modalidade_service: ModalidadeService,
        matricula_service: MatriculaService,
        faturamento_service: FaturamentoService,
    ):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.__botoes: dict[str, ctk.CTkButton] = {}

        self.__criar_menu()
        self.__criar_area_conteudo()
        self.__criar_views(
            aluno_service,
            professor_service,
            modalidade_service,
            matricula_service,
            faturamento_service,
        )

        self.__mostrar_view("Alunos")

    def __criar_menu(self) -> None:
        self.__menu = ctk.CTkFrame(
            self,
            width=210,
            corner_radius=0,
        )
        self.__menu.grid(
            row=0,
            column=0,
            sticky="ns",
        )
        self.__menu.grid_propagate(False)
        self.__menu.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self.__menu,
            text="PowerOn",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).grid(
            row=0,
            column=0,
            padx=20,
            pady=(30, 35),
            sticky="w",
        )

        opcoes = (
            "Alunos",
            "Professores",
            "Modalidades",
            "Matrículas",
            "Faturamento",
        )

        for linha, nome in enumerate(opcoes, start=1):
            botao = ctk.CTkButton(
                self.__menu,
                text=f"      {nome}",
                anchor="w",
                height=42,
                fg_color="transparent",
                command=lambda nome_view=nome: self.__mostrar_view(nome_view),
            )
            botao.grid(
                row=linha,
                column=0,
                padx=12,
                pady=5,
                sticky="ew",
            )

            self.__botoes[nome] = botao

    def __criar_area_conteudo(self) -> None:
        self.__conteudo = ctk.CTkFrame(
            self,
            fg_color="transparent",
            corner_radius=0,
        )
        self.__conteudo.grid(
            row=0,
            column=1,
            sticky="nsew",
        )
        self.__conteudo.grid_rowconfigure(0, weight=1)
        self.__conteudo.grid_columnconfigure(0, weight=1)

    def __criar_views(
        self,
        aluno_service: AlunoService,
        professor_service: ProfessorService,
        modalidade_service: ModalidadeService,
        matricula_service: MatriculaService,
        faturamento_service: FaturamentoService,
    ) -> None:
        self.__views = {
            "Alunos": AlunoView(
                self.__conteudo,
                aluno_service,
            ),
            "Professores": ProfessorView(
                self.__conteudo,
                professor_service,
            ),
            "Modalidades": ModalidadeView(
                self.__conteudo,
                modalidade_service,
            ),
            "Matrículas": MatriculaView(
                self.__conteudo,
                matricula_service,
            ),
            "Faturamento": FaturamentoView(
                self.__conteudo,
                faturamento_service,
            ),
        }

        for view in self.__views.values():
            view.grid(
                row=0,
                column=0,
                sticky="nsew",
            )

    def __mostrar_view(self, nome: str) -> None:
        view = self.__views[nome]
        view.tkraise()

        for nome_botao, botao in self.__botoes.items():
            if nome_botao == nome:
                botao.configure(
                    fg_color=("gray75", "gray25"),
                )
            else:
                botao.configure(
                    fg_color="transparent",
                )
