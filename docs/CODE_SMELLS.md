# Prevenção de code smells

| Smell | Medida preventiva neste projeto |
|---|---|
| Long Method | ruff `PLR0915` (máx. 15 instruções); métodos de 2–6 linhas |
| Long Parameter List | ruff `PLR0913` (máx. 4); `gerar_escala` agrupa o contexto em `Ciclo`/`Escala` |
| Large Class / God Class | uma responsabilidade por arquivo; `_Distribuidor` só distribui |
| Complexidade ciclomática | ruff `C901` (máx. 5) |
| Magic Numbers | ruff `PLR2004`; constantes `PESO_MINIMO`, `PESO_MAXIMO`, `DIAS_POR_PERIODICIDADE` |
| Primitive Obsession | `Periodicidade` (Enum), `Ciclo`, `Atribuicao` em vez de strings/tuplas soltas |
| Data Clumps | `(inicio, fim)` virou `Ciclo` |
| Duplicated Code | regra de "ativo" e de elegibilidade em um único lugar |
| Feature Envy | cálculo de carga fica em `Escala.carga_por_morador`, não no algoritmo |
| Switch Statements | dicionário `DIAS_POR_PERIODICIDADE` no lugar de if/elif em cadeia |
| Mutable state / efeitos colaterais | dataclasses `frozen=True`, funções puras |
| Fat Controller / lógica na view | rotas Flask só convertem entrada e chamam `ServicoEscala`; regra de negócio fica no domínio |
| Divergent Change / Shotgun Surgery | camadas separadas (web → serviço → repositório → domínio); trocar persistência mexe só em `repositorio.py` |
| Duplicated Code entre API e páginas | ambas usam o mesmo `entrada.py` e o mesmo serviço |
| Magic Numbers nos testes | `HTTPStatus.CREATED` etc. no lugar de 201/400/404 |
| Comentários explicando código confuso | nomes expressivos; comentários só para regras de negócio |

Checklist de code review: rodar `ruff check .` antes de cada PR e revisar esta tabela.
