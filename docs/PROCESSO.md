# Processo aplicado (F3: RUP + Scrum + XP + Kanban)

| Fase RUP | O que foi feito neste módulo |
|---|---|
| Concepção | Escopo = F7 e F8 (+ NF6.1, NF7.1, NF7.2, NF8.1), IDs herdados da F1 |
| Elaboração | Casos de uso UC4 (Gerar escala), lista de riscos (RISCOS.md), matriz (RASTREABILIDADE.md) |
| Construção | 2 sprints curtas (abaixo), TDD, CI, quadro Kanban com WIP |
| Transição | Teste de aceitação com cenário de 3 moradores / 3 ciclos, avaliação de riscos residuais |

## Sprints (Scrum)
- **Sprint 1**: modelos + validação de peso (NF6.1) + ciclo/periodicidade (NF7.2).
- **Sprint 2**: algoritmo de rodízio (F7, NF7.1) + refatoração + documentação.
- **Sprint 3**: camada web Flask (serviço, repositório, API JSON e página) para F7/F8 e NF8.1.
Cada sprint: planning (revisa riscos), daily, review (atualiza a matriz), retrospectiva.

## Práticas XP usadas
- **TDD**: commit de teste falhando → commit da implementação → commit de refatoração.
- **Integração contínua**: `.github/workflows/ci.yml` roda ruff + pytest a cada push.
- **Refatoração** contínua guiada por `CODE_SMELLS.md`.
- **Programação em par** no algoritmo (registrar no PR/commit com `Co-authored-by`).
- **Spike** para decidir a estratégia do rodízio (alternativas na seção abaixo).

## Kanban (colunas e WIP)
`Backlog → Em andamento (WIP 3) → Testando (WIP 2) → Pronto`
Cada card cita o ID do requisito. Usar GitHub Projects no repositório.

## Convenção de commits (GRE3)
`[F7][NF7.1] test: não repete tarefa com mesma pessoa em ciclos seguidos`
`[F7][NF7.1] feat: exclui responsável anterior dos candidatos`
`[F7] refactor: extrai _candidatos_para`

## Spike: alternativas avaliadas
1. Round-robin puro (ignora peso) – descartado: não atende NF7.1.
2. Embaralhamento aleatório – descartado: não determinístico, difícil de testar.
3. **Guloso por menor carga (LPT) + exclusão do responsável anterior** – escolhido:
   simples, determinístico, limite de desequilíbrio ≤ maior peso.
