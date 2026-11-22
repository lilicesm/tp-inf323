"""Interface HTML simples (formulários) sobre o mesmo serviço da API."""
from collections.abc import Callable

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)

from escala.errors import EscalaError, EscalaNaoGeradaError
from escala.servico import ServicoEscala
from escala.web.entrada import ler_inicio_e_periodicidade, ler_morador, ler_tarefa

paginas = Blueprint("paginas", __name__)


def servico() -> ServicoEscala:
    return current_app.extensions["escala"]


@paginas.get("/")
def inicio():
    servico_atual = servico()
    return render_template(
        "index.html",
        moradores=servico_atual.moradores(),
        tarefas=servico_atual.tarefas(),
        escala=_escala_ou_nada(servico_atual),
        nomes=_nomes_por_id(servico_atual),
        destaque=request.args.get("morador"),  # NF8.1
    )


@paginas.post("/moradores")
def cadastrar_morador():
    return _executar(lambda: servico().cadastrar_morador(ler_morador(request.form)))


@paginas.post("/tarefas")
def cadastrar_tarefa():
    return _executar(lambda: servico().cadastrar_tarefa(*ler_tarefa(request.form)))


@paginas.post("/escalas")
def gerar_escala():
    def gerar():
        inicio, periodicidade = ler_inicio_e_periodicidade(request.form)
        servico().gerar_proxima_escala(inicio, periodicidade)

    return _executar(gerar)


def _executar(acao: Callable[[], object]):
    try:
        acao()
    except EscalaError as erro:
        flash(str(erro))
    return redirect(url_for("paginas.inicio"))


def _escala_ou_nada(servico_atual: ServicoEscala):
    try:
        return servico_atual.escala_atual()
    except EscalaNaoGeradaError:
        return None


def _nomes_por_id(servico_atual: ServicoEscala) -> dict[str, str]:
    entidades = [*servico_atual.moradores(), *servico_atual.tarefas()]
    return {entidade.id: entidade.nome for entidade in entidades}
