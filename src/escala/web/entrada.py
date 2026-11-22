"""Conversão dos dados recebidos (JSON ou formulário) em objetos de domínio."""
from collections.abc import Mapping
from datetime import date

from escala.ciclo import Periodicidade
from escala.errors import DadosInvalidosError


def ler_morador(dados: Mapping) -> str:
    return _texto(dados, "nome")


def ler_tarefa(dados: Mapping) -> tuple[str, int]:
    return _texto(dados, "nome"), _inteiro(dados, "peso")


def ler_inicio_e_periodicidade(dados: Mapping) -> tuple[date, Periodicidade]:
    return _data(dados, "inicio"), _periodicidade(dados, "periodicidade")


def _texto(dados: Mapping, campo: str) -> str:
    valor = str(dados.get(campo, "")).strip()
    if not valor:
        raise DadosInvalidosError(f"Campo obrigatório ausente: {campo}")
    return valor


def _inteiro(dados: Mapping, campo: str) -> int:
    try:
        return int(_texto(dados, campo))
    except ValueError as erro:
        mensagem = f"Campo {campo} deve ser um número inteiro"
        raise DadosInvalidosError(mensagem) from erro


def _data(dados: Mapping, campo: str) -> date:
    try:
        return date.fromisoformat(_texto(dados, campo))
    except ValueError as erro:
        mensagem = f"Campo {campo} deve estar no formato AAAA-MM-DD"
        raise DadosInvalidosError(mensagem) from erro


def _periodicidade(dados: Mapping, campo: str) -> Periodicidade:
    try:
        return Periodicidade(_texto(dados, campo))
    except ValueError as erro:
        opcoes = ", ".join(p.value for p in Periodicidade)
        raise DadosInvalidosError(f"Campo {campo} deve ser: {opcoes}") from erro
