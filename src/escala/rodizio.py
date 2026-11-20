"""Algoritmo de rodízio ponderado (F7, NF7.1).

Regras:
1. Tarefas mais pesadas são distribuídas primeiro.
2. Cada tarefa vai para o morador com menor carga no ciclo (balanceamento).
3. Nunca repete a mesma tarefa com a mesma pessoa em ciclos seguidos,
   salvo se ela for a única opção (um único morador ativo).
4. Empates são resolvidos em favor de quem teve MENOS carga no ciclo
   anterior (rodízio justo entre ciclos).
"""
from collections.abc import Iterable

from escala.ciclo import Ciclo
from escala.errors import SemMoradoresAtivosError
from escala.modelos import Atribuicao, Escala, Morador, Tarefa


def gerar_escala(
    moradores: Iterable[Morador],
    tarefas: Iterable[Tarefa],
    ciclo: Ciclo,
    escala_anterior: Escala | None = None,
) -> Escala:
    distribuidor = _Distribuidor(moradores, escala_anterior)
    return Escala(ciclo, distribuidor.distribuir(tarefas))


class _Distribuidor:
    def __init__(
        self, moradores: Iterable[Morador], escala_anterior: Escala | None
    ) -> None:
        self._anterior = escala_anterior
        self._moradores = self._ativos_por_desempate(moradores)
        self._carga = {m.id: 0 for m in self._moradores}

    def distribuir(self, tarefas: Iterable[Tarefa]) -> tuple[Atribuicao, ...]:
        ativas = [t for t in tarefas if t.ativa]
        mais_pesadas_primeiro = sorted(ativas, key=lambda t: (-t.peso, t.id))
        return tuple(self._atribuir(t) for t in mais_pesadas_primeiro)

    def _atribuir(self, tarefa: Tarefa) -> Atribuicao:
        candidatos = self._candidatos_para(tarefa)
        escolhido = min(candidatos, key=lambda m: self._carga[m.id])
        self._carga[escolhido.id] += tarefa.peso
        return Atribuicao(tarefa.id, escolhido.id, tarefa.peso)

    def _candidatos_para(self, tarefa: Tarefa) -> list[Morador]:
        anterior = self._responsavel_anterior(tarefa)
        elegiveis = [m for m in self._moradores if m.id != anterior]
        return elegiveis or self._moradores

    def _responsavel_anterior(self, tarefa: Tarefa) -> str | None:
        if self._anterior is None:
            return None
        return self._anterior.responsavel_pela(tarefa.id)

    def _ativos_por_desempate(self, moradores: Iterable[Morador]) -> list[Morador]:
        ativos = [m for m in moradores if m.ativo]
        if not ativos:
            raise SemMoradoresAtivosError("Nenhum morador ativo na república")
        carga_anterior = self._anterior.carga_por_morador() if self._anterior else {}
        return sorted(ativos, key=lambda m: (carga_anterior.get(m.id, 0), m.id))
