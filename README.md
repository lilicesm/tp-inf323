# República – Módulo de Escala de Rodízio Ponderado

INF 323 – Engenharia de Software II (F4: implementação de um módulo).

Módulo escolhido: **geração e consulta da escala de rodízio (F7 e F8)**, com os requisitos
NF7.1 (rodízio ponderado, sem repetir tarefa/pessoa em ciclos seguidos),
NF7.2 (periodicidade semanal/quinzenal/mensal), NF6.1 (peso 1 a 5) e
NF8.1 (destaque das tarefas do morador).
É o módulo do Ciclo 2 do planejamento da F1 e o risco técnico da lista da F3.

Implementado em **Python + Flask**, seguindo o processo da F3 (RUP + Scrum + XP + Kanban).
Ver [docs/PROCESSO.md](docs/PROCESSO.md).

## Como rodar

Windows (PowerShell):

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1   # Trocar essa linha pelo usado no seu sistema
pip install -e ".[dev]"
flask --app escala.web run      # abre em http://127.0.0.1:5000
```

Linux/macOS: troque a ativação por `source .venv/bin/activate`.

## Testes e qualidade

```bash
pytest --cov=escala --cov-report=term-missing   # 53 testes, 100% de cobertura
ruff check .                                     # regras anti code smell
```

Cada teste tem `@pytest.mark.requisito("F7", "NF7.1", ...)`, o que liga o teste ao requisito (GRE3).

## API web

| Método | Rota | Requisito | Corpo (JSON) |
|---|---|---|---|
| POST | `/api/moradores` | F4 | `{"nome": "Ana"}` |
| POST | `/api/tarefas` | F6, NF6.1 | `{"nome": "Cozinha", "peso": 5}` |
| POST | `/api/escalas` | F7, NF7.1, NF7.2 | `{"inicio": "2026-11-23", "periodicidade": "semanal"}` |
| GET | `/api/escalas/atual` | F8 | – |
| GET | `/api/moradores/<id>/tarefas` | F8, NF8.1 | – |

Erros: `400` dados inválidos, `404` sem escala gerada. Corpo: `{"erro": "..."}`.

A página `/` oferece os mesmos cadastros por formulário e mostra a escala atual.
`/?morador=m1` destaca as tarefas desse morador (NF8.1).

Os dados ficam em memória (`RepositorioEmMemoria`). Trocar por um banco de dados exige mudar só essa classe.

## Algoritmo (NF7.1)

1. Tarefas mais pesadas primeiro.
2. Cada tarefa vai para o morador de menor carga acumulada no ciclo.
3. Quem fez a tarefa no ciclo anterior é excluído (exceto se for o único morador ativo).
4. Empates: vence quem teve menor carga no ciclo anterior.

Garantia testada: a diferença entre a maior e a menor carga nunca passa do maior peso (5).
Quando a regra 3 entra em conflito com o balanceamento perfeito, a regra 3 tem prioridade (é requisito).

## Arquitetura

```
web (Flask)      escala/web/      api.py · paginas.py · entrada.py · templates/
aplicação        escala/servico.py          casos de uso (cadastrar, gerar, consultar)
persistência     escala/repositorio.py      em memória
domínio          escala/modelos.py · ciclo.py · rodizio.py · errors.py
```

A dependência vai sempre de cima para baixo. O domínio não conhece Flask e é testado sem servidor.

```
tests/   um arquivo por módulo; cada teste cita o ID do requisito
docs/    PROCESSO.md · RASTREABILIDADE.md · RISCOS.md · CODE_SMELLS.md
```
