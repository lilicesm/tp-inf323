import pytest

from conftest import morador, tarefa
from escala import gerar_escala
from escala.errors import SemMoradoresAtivosError
from escala.modelos import PESO_MAXIMO


def _ids_atribuidos(escala):
    return [a.tarefa_id for a in escala.atribuicoes]


@pytest.mark.requisito("F7")
def test_cada_tarefa_ativa_recebe_exatamente_um_responsavel(ciclo):
    tarefas = [tarefa("t1", 3), tarefa("t2", 2), tarefa("t3", 1)]
    escala = gerar_escala([morador("A"), morador("B")], tarefas, ciclo)
    assert sorted(_ids_atribuidos(escala)) == ["t1", "t2", "t3"]


@pytest.mark.requisito("F7", "F23")
def test_ignora_moradores_inativos(ciclo):
    escala = gerar_escala(
        [morador("A"), morador("B", ativo=False)], [tarefa("t1", 3)], ciclo
    )
    assert escala.responsavel_pela("t1") == "A"


@pytest.mark.requisito("F6", "F7")
def test_ignora_tarefas_desativadas(ciclo):
    escala = gerar_escala(
        [morador("A")], [tarefa("t1", 3), tarefa("t2", 2, ativa=False)], ciclo
    )
    assert _ids_atribuidos(escala) == ["t1"]


@pytest.mark.requisito("F7")
def test_escala_sem_tarefas_ativas_e_vazia(ciclo):
    assert gerar_escala([morador("A")], [], ciclo).atribuicoes == ()


@pytest.mark.requisito("F7")
def test_falha_sem_moradores_ativos(ciclo):
    with pytest.raises(SemMoradoresAtivosError):
        gerar_escala([morador("A", ativo=False)], [tarefa("t1", 1)], ciclo)


@pytest.mark.requisito("F7", "NF7.1")
def test_balanceia_carga_entre_dois_moradores(ciclo):
    tarefas = [tarefa("t1", 4), tarefa("t2", 3), tarefa("t3", 2), tarefa("t4", 1)]
    escala = gerar_escala([morador("A"), morador("B")], tarefas, ciclo)
    assert escala.carga_por_morador() == {"A": 5, "B": 5}


@pytest.mark.requisito("F7", "NF7.1")
def test_diferenca_de_carga_nunca_excede_o_maior_peso(ciclo):
    moradores = [morador(i) for i in "ABCD"]
    pesos = [5, 4, 3, 3, 2, 2, 1, 1, 1]
    tarefas = [tarefa(f"t{n}", p) for n, p in enumerate(pesos)]
    carga = gerar_escala(moradores, tarefas, ciclo).carga_por_morador()
    assert max(carga.values()) - min(carga.values()) <= PESO_MAXIMO


@pytest.mark.requisito("F7", "NF7.1")
def test_nao_repete_tarefa_com_mesma_pessoa_em_ciclos_seguidos(ciclo):
    moradores = [morador("A"), morador("B"), morador("C")]
    tarefas = [tarefa("t1", 5), tarefa("t2", 3), tarefa("t3", 1)]
    anterior = gerar_escala(moradores, tarefas, ciclo)
    atual = gerar_escala(moradores, tarefas, ciclo, escala_anterior=anterior)
    for t in tarefas:
        assert atual.responsavel_pela(t.id) != anterior.responsavel_pela(t.id)


@pytest.mark.requisito("F7", "NF7.1")
def test_unico_morador_pode_repetir_tarefa(ciclo):
    moradores = [morador("A")]
    tarefas = [tarefa("t1", 2)]
    anterior = gerar_escala(moradores, tarefas, ciclo)
    atual = gerar_escala(moradores, tarefas, ciclo, escala_anterior=anterior)
    assert atual.responsavel_pela("t1") == "A"


@pytest.mark.requisito("F7", "NF7.1")
def test_empate_favorece_quem_teve_menos_carga_no_ciclo_anterior(ciclo):
    moradores = [morador("A"), morador("B")]
    anterior = gerar_escala(
        moradores, [tarefa("x", 5), tarefa("y", 1)], ciclo
    )  # A fez x (5), B fez y (1)
    atual = gerar_escala(moradores, [tarefa("z", 2)], ciclo, escala_anterior=anterior)
    assert atual.responsavel_pela("z") == "B"


@pytest.mark.requisito("F7", "F23")
def test_escala_anterior_com_morador_removido_nao_quebra(ciclo):
    anterior = gerar_escala([morador("A"), morador("B")], [tarefa("t1", 3)], ciclo)
    atual = gerar_escala([morador("C")], [tarefa("t1", 3)], ciclo, anterior)
    assert atual.responsavel_pela("t1") == "C"


@pytest.mark.requisito("F7")
def test_resultado_e_deterministico(ciclo):
    moradores = [morador("B"), morador("A")]
    tarefas = [tarefa("t2", 2), tarefa("t1", 2)]
    primeira = gerar_escala(moradores, tarefas, ciclo)
    segunda = gerar_escala(reversed(moradores), reversed(tarefas), ciclo)
    assert primeira == segunda
