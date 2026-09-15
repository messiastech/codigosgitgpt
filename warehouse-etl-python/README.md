# Warehouse ETL · pipeline de vendas

Pipeline CSV → validação → transformação → SQLite, com carga idempotente e auditoria de execução.

## Executar em 2 minutos

Requer Python 3.11 ou superior. Usa apenas a biblioteca padrão: nenhuma dependência externa.
Abra o terminal na pasta deste projeto.

```sh
python app.py examples/orders.csv --db warehouse.db
python app.py examples/orders.csv --db warehouse.db
# Segunda execução: 0 inserções, 3 registros já existentes
```

## Funcionalidades e decisões

- Chave order_id evita duplicação ao reprocessar arquivos.
- Valores monetários armazenados em centavos inteiros.
- Validação completa antes da carga; conflitos de conteúdo causam rollback.
- Cada execução bem-sucedida gera uma entrada na tabela runs.
- Datas ISO e preços com ponto decimal; arquivos são processados em memória.
- Demonstra carga batch local, sem orquestração distribuída.

## Testes

```sh
python -m unittest discover -s tests -v
```

Os testes usam diretórios temporários e não alteram seus dados. O fluxo de integração
contínua executa a mesma suíte em Python 3.11, 3.12 e 3.13.

## Estrutura

- `app.py`: aplicação e interface de execução.
- `tests/`: testes de comportamento e casos de erro.
- `examples/`: arquivos fictícios para experimentar.

Projeto de demonstração para portfólio. Leia as limitações acima antes de adaptar
para uso real. Dados de exemplo são fictícios.

## Arquitetura

Entrada CSV → extract (validação e centavos) → run (transação SQLite) → orders + runs. A mesma chave com valores diferentes é erro; não há atualização silenciosa.

## Demonstração em entrevista

Execute o exemplo, explique o fluxo acima e rode os testes. Mostre um caso inválido e como a aplicação preserva os dados ou informa o erro.
