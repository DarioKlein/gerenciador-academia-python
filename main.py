import customtkinter as ctk

from repositories import Repositorio, TipoRepositorio
from services import (
    AlunoService,
    ProfessorService,
    ModalidadeService,
    MatriculaService,
    FaturamentoService,
)
from views import PrincipalView

ctk.set_appearance_mode("system")
ctk.set_default_color_theme("tema.json")

repositorio_alunos = Repositorio(TipoRepositorio.ALUNO)
repositorio_professores = Repositorio(TipoRepositorio.PROFESSOR)
repositorio_modalidades = Repositorio(TipoRepositorio.MODALIDADE)
repositorio_matriculas = Repositorio(TipoRepositorio.MATRICULA)

aluno_service = AlunoService(repositorio_alunos, repositorio_matriculas)
professor_service = ProfessorService(repositorio_professores, repositorio_modalidades)

modalidade_service = ModalidadeService(
    repositorio_modalidades, repositorio_professores, repositorio_matriculas
)

matricula_service = MatriculaService(
    repositorio_matriculas,
    repositorio_alunos,
    repositorio_modalidades,
)

faturamento_service = FaturamentoService(
    modalidade_service,
    repositorio_matriculas,
)

janela = ctk.CTk()
janela.title("PowerOn — Gerenciador de Academia")
janela.geometry("1200x700")
janela.minsize(1200, 700)

janela.grid_rowconfigure(0, weight=1)
janela.grid_columnconfigure(0, weight=1)

principal_view = PrincipalView(
    janela,
    aluno_service,
    professor_service,
    modalidade_service,
    matricula_service,
    faturamento_service,
)
principal_view.grid(
    row=0,
    column=0,
    sticky="nsew",
)

janela.mainloop()
