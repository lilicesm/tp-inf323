"""API REST/JSON do módulo de escala."""
from flask import Blueprint, current_app, jsonify, request

from escala.errors import EscalaError, EscalaNaoGeradaError
from escala.modelos import Atribuicao, Escala
from escala.servico import ServicoEscala
from escala.web.entrada import ler_inicio_e_periodicidade, ler_morador, ler_tarefa

api = Blueprint("api", __name__, url_prefix="/api")

HTTP_CRIADO = 201
HTTP_REQUISICAO_INVALIDA = 400
STATUS_POR_ERRO = {EscalaNaoGeradaError: 404}


def servico() -> ServicoEscala:
    return current_app.extensions["escala"]


@api.errorhandler(EscalaError)
def tratar_erro_de_dominio(erro: EscalaError):
    status = STATUS_POR_ERRO.get(type(erro), HTTP_REQUISICAO_INVALIDA)
    return jsonify(erro=str(erro)), status


@api.post("/moradores")
def cadastrar_morador():
    morador = servico().cadastrar_morador(ler_morador(_corpo_json()))
    return jsonify(id=morador.id, nome=morador.nome), HTTP_CRIADO


@api.post("/tarefas")  # F6, NF6.1
def cadastrar_tarefa():
    tarefa = servico().cadastrar_tarefa(*ler_tarefa(_corpo_json()))
    return jsonify(id=tarefa.id, nome=tarefa.nome, peso=tarefa.peso), HTTP_CRIADO


@api.post("/escalas")  # F7, NF7.1, NF7.2
def gerar_escala():
    inicio, periodicidade = ler_inicio_e_periodicidade(_corpo_json())
    escala = servico().gerar_proxima_escala(inicio, periodicidade)
    return jsonify(escala_json(escala)), HTTP_CRIADO


@api.get("/escalas/atual")  # F8
def consultar_escala_atual():
    return jsonify(escala_json(servico().escala_atual()))


@api.get("/moradores/<morador_id>/tarefas")  # F8
def consultar_tarefas_do_morador(morador_id: str):
    atribuicoes = servico().tarefas_do_morador(morador_id)
    return jsonify([atribuicao_json(a) for a in atribuicoes])


def escala_json(escala: Escala) -> dict:
    return {
        "inicio": escala.ciclo.inicio.isoformat(),
        "fim": escala.ciclo.fim.isoformat(),
        "atribuicoes": [atribuicao_json(a) for a in escala.atribuicoes],
    }


def atribuicao_json(atribuicao: Atribuicao) -> dict:
    return {
        "tarefa_id": atribuicao.tarefa_id,
        "morador_id": atribuicao.morador_id,
        "peso": atribuicao.peso,
    }


def _corpo_json() -> dict:
    return request.get_json(silent=True) or {}
