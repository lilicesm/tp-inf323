"""Entidades do domínio (imutáveis, para evitar efeitos colaterais)."""
from dataclasses import dataclass

from escala.ciclo import Ciclo
from escala.errors import PesoInvalidoError

PESO_MINIMO = 1
PESO_MAXIMO = 5


@dataclass(frozen=True)
class Morador:
    id: str
    nome: str
    ativo: bool = True


@dataclass(frozen=True)
class Tarefa:
    id: str
    nome: str
    peso: int
    ativa: bool = True

    def __post_init__(self) -> None:
        if not PESO_MINIMO <= self.peso <= PESO_MAXIMO:
            raise PesoInvalidoError(
                f"Peso {self.peso} fora do intervalo {PESO_MINIMO}-{PESO_MAXIMO}"
            )


@dataclass(frozen=True)
class Atribuicao:
    tarefa_id: str
    morador_id: str
    peso: int


@dataclass(frozen=True)
class Escala:
    ciclo: Ciclo
    atribuicoes: tuple[Atribuicao, ...]

    def responsavel_pela(self, tarefa_id: str) -> str | None:
        for atribuicao in self.atribuicoes:
            if atribuicao.tarefa_id == tarefa_id:
                return atribuicao.morador_id
        return None

    def carga_por_morador(self) -> dict[str, int]:
        carga: dict[str, int] = {}
        for atribuicao in self.atribuicoes:
            carga[atribuicao.morador_id] = (
                carga.get(atribuicao.morador_id, 0) + atribuicao.peso
            )
        return carga
