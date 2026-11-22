from datetime import date

import pytest

from escala import Periodicidade
from escala.errors import EscalaNaoGeradaError
from escala.repositorio import RepositorioEmMemoria
from escala.servico import ServicoEscala

SEGUNDA = date(2026, 11, 23)


@pytest.fixture
def servico():
    servico = ServicoEscala(RepositorioEmMemoria())
    for nome in ["Ana", "Beto", "Caio"]:
        servico.cadastrar_morador(nome)
    for nome, peso in [("Cozinha", 5), ("Banheiro", 3), ("Lixo", 1)]:
        servico.cadastrar_tarefa(nome, peso)
    return servico


@pytest.mark.requisito("F4", "F6")
def test_cadastro_gera_ids_unicos_mesmo_com_nomes_repetidos(servico):
    primeiro = servico.cadastrar_morador("Ana")
    segundo = servico.cadastrar_morador("Ana")
    tarefa_a = servico.cadastrar_tarefa("Lixo", 2)
    tarefa_b = servico.cadastrar_tarefa("Lixo", 2)
    assert primeiro.id != segundo.id
    assert tarefa_a.id != tarefa_b.id


@pytest.mark.requisito("F7", "NF7.2")
def test_gera_escala_com_periodicidade_escolhida(servico):
    escala = servico.gerar_proxima_escala(SEGUNDA, Periodicidade.QUINZENAL)
    assert escala.ciclo.fim == date(2026, 12, 6)
    assert len(escala.atribuicoes) == len(servico.tarefas())


@pytest.mark.requisito("F7", "NF7.1")
def test_proxima_escala_usa_a_anterior_para_nao_repetir(servico):
    primeira = servico.gerar_proxima_escala(SEGUNDA, Periodicidade.SEMANAL)
    segunda = servico.gerar_proxima_escala(date(2026, 11, 30), Periodicidade.SEMANAL)
    for t in servico.tarefas():
        assert segunda.responsavel_pela(t.id) != primeira.responsavel_pela(t.id)


@pytest.mark.requisito("F8")
def test_escala_atual_e_a_ultima_gerada(servico):
    servico.gerar_proxima_escala(SEGUNDA, Periodicidade.SEMANAL)
    ultima = servico.gerar_proxima_escala(date(2026, 11, 30), Periodicidade.SEMANAL)
    assert servico.escala_atual() == ultima


@pytest.mark.requisito("F8")
def test_consultar_antes_de_gerar_falha(servico):
    with pytest.raises(EscalaNaoGeradaError):
        servico.escala_atual()


@pytest.mark.requisito("F8", "NF8.1")
def test_tarefas_do_morador_filtra_pelo_responsavel(servico):
    escala = servico.gerar_proxima_escala(SEGUNDA, Periodicidade.SEMANAL)
    responsavel = escala.responsavel_pela(servico.tarefas()[0].id)
    tarefas = servico.tarefas_do_morador(responsavel)
    assert tarefas
    assert all(a.morador_id == responsavel for a in tarefas)
