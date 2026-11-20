# Lista de riscos (GPR6)

| ID | Risco | Prob. | Impacto | Prioridade | Tratamento |
|---|---|---|---|---|---|
| R1 | Algoritmo gera escala desbalanceada | Média | Alto | Alta | Spike + teste de propriedade (diferença ≤ maior peso) |
| R2 | Regra "não repetir" inviabiliza distribuição (ex.: 1 morador) | Média | Médio | Média | Fallback documentado e testado |
| R3 | Resultado não determinístico, testes instáveis | Baixa | Alto | Média | Desempate por (carga anterior, id); teste de determinismo |
| R4 | Datas de ciclo erradas (fim de mês, virada de ano) | Média | Médio | Média | Testes parametrizados com 31/01 e dezembro |
| R5 | Estimativa subestimada (F1: 2,21 h/PF vs F2: 6,5 h/PF) | Alta | Alto | Alta | Acompanhar burndown em horas; ação corretiva na retrospectiva |

Revisar a cada planning/retrospectiva; riscos materializados viram card no Kanban.
