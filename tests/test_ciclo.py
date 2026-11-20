from datetime import date

import pytest

from escala import Ciclo, Periodicidade, criar_ciclo
from escala.errors import CicloInvalidoError


@pytest.mark.requisito("F7", "NF7.2")
@pytest.mark.parametrize(
    ("inicio", "periodicidade", "fim"),
    [
        (date(2026, 11, 23), Periodicidade.SEMANAL, date(2026, 11, 29)),
        (date(2026, 11, 23), Periodicidade.QUINZENAL, date(2026, 12, 6)),
        (date(2026, 1, 1), Periodicidade.MENSAL, date(2026, 1, 31)),
        (date(2026, 1, 31), Periodicidade.MENSAL, date(2026, 2, 27)),
        (date(2026, 12, 15), Periodicidade.MENSAL, date(2027, 1, 14)),
    ],
)
def test_fim_do_ciclo_conforme_periodicidade(inicio, periodicidade, fim):
    assert criar_ciclo(inicio, periodicidade).fim == fim


@pytest.mark.requisito("F7", "NF7.2")
def test_rejeita_ciclo_com_fim_antes_do_inicio():
    with pytest.raises(CicloInvalidoError):
        Ciclo(date(2026, 11, 23), date(2026, 11, 22))
