from http import HTTPStatus

import pytest

from escala.web import create_app

CICLO = {"inicio": "2026-11-23", "periodicidade": "semanal"}


@pytest.fixture
def cliente():
    app = create_app()
    app.testing = True
    return app.test_client()


@pytest.fixture
def cliente_com_dados(cliente):
    for nome in ["Ana", "Beto"]:
        cliente.post("/api/moradores", json={"nome": nome})
    for nome, peso in [("Cozinha", 4), ("Lixo", 2)]:
        cliente.post("/api/tarefas", json={"nome": nome, "peso": peso})
    return cliente


# --- API JSON -----------------------------------------------------------------


@pytest.mark.requisito("F6", "NF6.1")
def test_api_cadastra_tarefa(cliente):
    resposta = cliente.post("/api/tarefas", json={"nome": "Cozinha", "peso": 5})
    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.get_json() == {"id": "t1", "nome": "Cozinha", "peso": 5}


@pytest.mark.requisito("F6", "NF6.1")
def test_api_rejeita_peso_invalido_com_400(cliente):
    resposta = cliente.post("/api/tarefas", json={"nome": "X", "peso": 7})
    assert resposta.status_code == HTTPStatus.BAD_REQUEST
    assert "Peso" in resposta.get_json()["erro"]


@pytest.mark.requisito("F4")
def test_api_cadastra_morador_com_id_gerado(cliente):
    resposta = cliente.post("/api/moradores", json={"nome": "Ana"})
    assert resposta.status_code == HTTPStatus.CREATED
    assert resposta.get_json() == {"id": "m1", "nome": "Ana"}


@pytest.mark.requisito("F4")
def test_api_sem_corpo_json_retorna_400(cliente):
    resposta = cliente.post("/api/moradores", data="texto")
    assert resposta.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.requisito("F7", "NF7.1", "NF7.2")
def test_api_gera_escala_balanceada(cliente_com_dados):
    resposta = cliente_com_dados.post("/api/escalas", json=CICLO)
    corpo = resposta.get_json()
    assert resposta.status_code == HTTPStatus.CREATED
    assert corpo["fim"] == "2026-11-29"
    responsaveis = {a["morador_id"] for a in corpo["atribuicoes"]}
    assert responsaveis == {"m1", "m2"}


@pytest.mark.requisito("F7")
def test_api_gerar_sem_moradores_retorna_400(cliente):
    resposta = cliente.post("/api/escalas", json=CICLO)
    assert resposta.status_code == HTTPStatus.BAD_REQUEST


@pytest.mark.requisito("F8")
def test_api_consulta_escala_atual(cliente_com_dados):
    gerada = cliente_com_dados.post("/api/escalas", json=CICLO).get_json()
    assert cliente_com_dados.get("/api/escalas/atual").get_json() == gerada


@pytest.mark.requisito("F8")
def test_api_consulta_sem_escala_retorna_404(cliente):
    assert cliente.get("/api/escalas/atual").status_code == HTTPStatus.NOT_FOUND


@pytest.mark.requisito("F8", "NF8.1")
def test_api_lista_tarefas_do_morador(cliente_com_dados):
    cliente_com_dados.post("/api/escalas", json=CICLO)
    tarefas = cliente_com_dados.get("/api/moradores/m1/tarefas").get_json()
    assert [t["morador_id"] for t in tarefas] == ["m1"] * len(tarefas)


# --- Páginas HTML -------------------------------------------------------------


@pytest.mark.requisito("F8")
def test_pagina_inicial_sem_escala(cliente):
    resposta = cliente.get("/")
    assert resposta.status_code == HTTPStatus.OK
    assert "Nenhuma escala gerada ainda" in resposta.get_data(as_text=True)


@pytest.mark.requisito("F7", "F8")
def test_formulario_gera_escala_e_mostra_nomes(cliente_com_dados):
    resposta = cliente_com_dados.post("/escalas", data=CICLO, follow_redirects=True)
    html = resposta.get_data(as_text=True)
    assert "23/11/2026 a 29/11/2026" in html
    assert "Cozinha" in html and "Ana" in html


@pytest.mark.requisito("F6", "NF6.1")
def test_formulario_mostra_erro_de_validacao(cliente):
    resposta = cliente.post(
        "/tarefas", data={"nome": "X", "peso": "0"}, follow_redirects=True
    )
    assert "fora do intervalo" in resposta.get_data(as_text=True)


@pytest.mark.requisito("F4", "F6")
def test_formularios_de_cadastro_redirecionam(cliente):
    morador = cliente.post("/moradores", data={"nome": "Ana"})
    tarefa = cliente.post("/tarefas", data={"nome": "Lixo", "peso": "2"})
    assert morador.status_code == tarefa.status_code == HTTPStatus.FOUND


@pytest.mark.requisito("F8", "NF8.1")
def test_pagina_destaca_tarefas_do_morador_escolhido(cliente_com_dados):
    cliente_com_dados.post("/escalas", data=CICLO)
    html = cliente_com_dados.get("/?morador=m1").get_data(as_text=True)
    assert 'class="destaque"' in html
