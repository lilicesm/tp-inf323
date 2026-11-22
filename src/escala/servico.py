"""Casos de uso do módulo (camada de aplicação entre a web e o domínio)."""
from datetime import date

from escala.ciclo import Periodicidade, criar_ciclo
from escala.errors import EscalaNaoGeradaError
from escala.modelos import Atribuicao, Escala, Morador, Tarefa
from escala.repositorio import RepositorioEmMemoria
from escala.rodizio import gerar_escala


class ServicoEscala:
    def __init__(self, repositorio: RepositorioEmMemoria) -> None:
        self._repo = repositorio

    def cadastrar_morador(self, nome: str) -> Morador:
        return self._repo.adicionar_morador(nome)

    def cadastrar_tarefa(self, nome: str, peso: int) -> Tarefa:  # F6
        return self._repo.adicionar_tarefa(nome, peso)

    def gerar_proxima_escala(  # F7, NF7.2
        self, inicio: date, periodicidade: Periodicidade
    ) -> Escala:
        escala = gerar_escala(
            self._repo.moradores(),
            self._repo.tarefas(),
            criar_ciclo(inicio, periodicidade),
            escala_anterior=self._repo.ultima_escala(),
        )
        self._repo.adicionar_escala(escala)
        return escala

    def escala_atual(self) -> Escala:  # F8
        escala = self._repo.ultima_escala()
        if escala is None:
            raise EscalaNaoGeradaError("Nenhuma escala foi gerada ainda")
        return escala

    def tarefas_do_morador(self, morador_id: str) -> list[Atribuicao]:  # F8
        return [
            a for a in self.escala_atual().atribuicoes if a.morador_id == morador_id
        ]

    def moradores(self) -> list[Morador]:
        return self._repo.moradores()

    def tarefas(self) -> list[Tarefa]:
        return self._repo.tarefas()
