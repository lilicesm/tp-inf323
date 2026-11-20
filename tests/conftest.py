from datetime import date

import pytest

from escala import Morador, Periodicidade, Tarefa, criar_ciclo


@pytest.fixture
def ciclo():
    return criar_ciclo(date(2026, 11, 23), Periodicidade.SEMANAL)


def morador(id_: str, ativo: bool = True) -> Morador:
    return Morador(id_, f"Morador {id_}", ativo)


def tarefa(id_: str, peso: int, ativa: bool = True) -> Tarefa:
    return Tarefa(id_, f"Tarefa {id_}", peso, ativa)
