"""Armazenamento em memória (substituível por banco de dados sem mudar o serviço)."""
from itertools import count

from escala.modelos import Escala, Morador, Tarefa


class RepositorioEmMemoria:
    def __init__(self) -> None:
        self._moradores: dict[str, Morador] = {}
        self._tarefas: dict[str, Tarefa] = {}
        self._escalas: list[Escala] = []
        self._proximo_morador = count(1)
        self._proxima_tarefa = count(1)

    def adicionar_morador(self, nome: str) -> Morador:
        morador = Morador(f"m{next(self._proximo_morador)}", nome)
        self._moradores[morador.id] = morador
        return morador

    def adicionar_tarefa(self, nome: str, peso: int) -> Tarefa:
        tarefa = Tarefa(f"t{next(self._proxima_tarefa)}", nome, peso)
        self._tarefas[tarefa.id] = tarefa
        return tarefa

    def adicionar_escala(self, escala: Escala) -> None:
        self._escalas.append(escala)

    def moradores(self) -> list[Morador]:
        return list(self._moradores.values())

    def tarefas(self) -> list[Tarefa]:
        return list(self._tarefas.values())

    def ultima_escala(self) -> Escala | None:
        return self._escalas[-1] if self._escalas else None

