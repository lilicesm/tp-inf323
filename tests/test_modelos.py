import pytest

from conftest import tarefa
from escala.errors import PesoInvalidoError


@pytest.mark.requisito("F6", "NF6.1")
@pytest.mark.parametrize("peso", [1, 3, 5])
def test_aceita_pesos_validos(peso):
    assert tarefa("t1", peso).peso == peso


@pytest.mark.requisito("F6", "NF6.1")
@pytest.mark.parametrize("peso", [0, 6, -1])
def test_rejeita_pesos_fora_do_intervalo(peso):
    with pytest.raises(PesoInvalidoError):
        tarefa("t1", peso)
