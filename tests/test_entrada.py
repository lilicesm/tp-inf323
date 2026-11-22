from datetime import date

import pytest

from escala import Periodicidade
from escala.errors import DadosInvalidosError
from escala.web.entrada import ler_inicio_e_periodicidade, ler_morador, ler_tarefa


@pytest.mark.requisito("F6", "NF6.1")
def test_le_tarefa_convertendo_peso_para_inteiro():
    peso = 3
    assert ler_tarefa({"nome": "Lixo", "peso": str(peso)}) == ("Lixo", peso)


@pytest.mark.requisito("F6", "NF6.1")
def test_peso_nao_numerico_e_invalido():
    with pytest.raises(DadosInvalidosError):
        ler_tarefa({"nome": "Lixo", "peso": "pesado"})


@pytest.mark.requisito("F6", "NF6.1")
def test_leitura_nao_valida_o_intervalo_do_peso():
    assert ler_tarefa({"nome": "Lixo", "peso": 9}) == ("Lixo", 9)


@pytest.mark.requisito("F4")
@pytest.mark.parametrize("dados", [{}, {"id": "A"}, {"nome": "  "}])
def test_morador_exige_nome(dados):
    with pytest.raises(DadosInvalidosError):
        ler_morador(dados)


@pytest.mark.requisito("F7", "NF7.2")
def test_le_inicio_e_periodicidade():
    dados = {"inicio": "2026-11-23", "periodicidade": "mensal"}
    assert ler_inicio_e_periodicidade(dados) == (
        date(2026, 11, 23),
        Periodicidade.MENSAL,
    )


@pytest.mark.requisito("F7", "NF7.2")
@pytest.mark.parametrize(
    "dados",
    [
        {"inicio": "23/11/2026", "periodicidade": "semanal"},
        {"inicio": "2026-11-23", "periodicidade": "diaria"},
    ],
)
def test_rejeita_data_ou_periodicidade_invalidas(dados):
    with pytest.raises(DadosInvalidosError):
        ler_inicio_e_periodicidade(dados)
