"""Erros de domínio do módulo de escala."""


class EscalaError(Exception):
    """Base de todos os erros do módulo."""


class PesoInvalidoError(EscalaError, ValueError):
    """Peso da tarefa fora do intervalo permitido (NF6.1)."""


class CicloInvalidoError(EscalaError, ValueError):
    """Ciclo com data final anterior à inicial."""


class SemMoradoresAtivosError(EscalaError):
    """Não há moradores ativos para receber tarefas."""


class CadastroDuplicadoError(EscalaError):
    """Já existe morador ou tarefa com o mesmo id."""


class EscalaNaoGeradaError(EscalaError):
    """Consulta de escala antes de qualquer escala ter sido gerada."""


class DadosInvalidosError(EscalaError, ValueError):
    """Dados recebidos pela web ausentes ou em formato inválido."""
