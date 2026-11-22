# Matriz de rastreabilidade (GRE3)

| Requisito | Caso de uso | Código | Testes |
|---|---|---|---|
| F4 (cadastro de morador na república) | UC2 | `servico.cadastrar_morador`, `POST /api/moradores`, `POST /moradores` | `test_cadastro_gera_ids_unicos_*`, `test_api_cadastra_morador_com_id_gerado`, `test_morador_exige_nome` |
| F6 / NF6.1 (peso 1–5) | UC3 | `modelos.Tarefa.__post_init__`, `entrada.ler_tarefa`, `POST /api/tarefas` | `test_modelos.py`, `test_entrada.py`, `test_api_cadastra_tarefa`, `test_api_rejeita_peso_invalido_com_400`, `test_formulario_mostra_erro_de_validacao` |
| F7 (gerar escala) | UC4 | `rodizio.gerar_escala`, `servico.gerar_proxima_escala`, `POST /api/escalas` | `test_rodizio.py`, `test_servico.py`, `test_api_gera_escala_balanceada` |
| NF7.1 (rodízio ponderado, sem repetição) | UC4 | `rodizio._Distribuidor`; serviço passa a escala anterior | `test_balanceia_*`, `test_diferenca_*`, `test_nao_repete_*`, `test_unico_morador_*`, `test_empate_*`, `test_proxima_escala_usa_a_anterior_*` |
| NF7.2 (periodicidade) | UC4 | `ciclo.criar_ciclo`, `entrada.ler_inicio_e_periodicidade` | `test_ciclo.py`, `test_le_inicio_e_periodicidade`, `test_rejeita_data_ou_periodicidade_invalidas` |
| F8 (consultar escala) | UC5 | `servico.escala_atual`, `GET /api/escalas/atual`, página `/` | `test_escala_atual_*`, `test_consultar_antes_de_gerar_falha`, `test_api_consulta_*`, `test_pagina_inicial_sem_escala` |
| NF8.1 (destaque das tarefas do morador) | UC5 | `servico.tarefas_do_morador`, `GET /api/moradores/<id>/tarefas`, `/?morador=` | `test_tarefas_do_morador_*`, `test_api_lista_tarefas_do_morador`, `test_pagina_destaca_*` |
| F23 (moradores inativos) | UC2 | filtro `ativo` em `_ativos_por_desempate` | `test_ignora_moradores_inativos`, `test_escala_anterior_com_morador_removido_*` |

Rastreio inverso: todo teste tem `@pytest.mark.requisito(...)`.
Listar testes de um requisito: `grep -rn '"NF7.1"' tests/`.
Commits citam o ID no prefixo (ver PROCESSO.md).
