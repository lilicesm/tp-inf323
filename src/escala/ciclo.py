"""Periodicidade e datas do ciclo da escala (NF7.2)."""
import calendar
from dataclasses import dataclass
from datetime import date, timedelta
from enum import Enum

from escala.errors import CicloInvalidoError


class Periodicidade(Enum):
    SEMANAL = "semanal"
    QUINZENAL = "quinzenal"
    MENSAL = "mensal"


DIAS_POR_PERIODICIDADE = {
    Periodicidade.SEMANAL: 7,
    Periodicidade.QUINZENAL: 14,
}
UM_DIA = timedelta(days=1)
MESES_NO_ANO = 12


@dataclass(frozen=True)
class Ciclo:
    inicio: date
    fim: date  # inclusivo

    def __post_init__(self) -> None:
        if self.fim < self.inicio:
            raise CicloInvalidoError("O fim do ciclo é anterior ao início")


def criar_ciclo(inicio: date, periodicidade: Periodicidade) -> Ciclo:
    return Ciclo(inicio, _proximo_inicio(inicio, periodicidade) - UM_DIA)


def _proximo_inicio(inicio: date, periodicidade: Periodicidade) -> date:
    if periodicidade is Periodicidade.MENSAL:
        return _somar_um_mes(inicio)
    return inicio + timedelta(days=DIAS_POR_PERIODICIDADE[periodicidade])


def _somar_um_mes(data: date) -> date:
    ano = data.year + data.month // MESES_NO_ANO
    mes = data.month % MESES_NO_ANO + 1
    ultimo_dia = calendar.monthrange(ano, mes)[1]
    return date(ano, mes, min(data.day, ultimo_dia))
