# Sales Insights · relatório de vendas

Transforma um CSV de vendas em relatório HTML independente, com indicadores e ranking de produtos.

## Executar em 2 minutos

Requer Python 3.11 ou superior. Usa apenas a biblioteca padrão: nenhuma dependência externa.
Abra o terminal na pasta deste projeto.

```sh
python app.py examples/sales.csv --output report.html
# Abra report.html no navegador
```

## Funcionalidades e decisões

- Valida esquema, datas ISO, valores monetários e quantidades.
- Decimal evita erros de ponto flutuante em dinheiro.
- HTML escapa nomes de produtos e inclui barras proporcionais.
- Um CSV inválido interrompe o relatório com número da linha.
- Valores usam ponto decimal; não inclui devoluções nem conversão cambial.

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

CSV → analyze (validação e agregação Decimal) → render (HTML escapado) → relatório independente. Agregações por produto e mês.

## Demonstração em entrevista

Execute o exemplo, explique o fluxo acima e rode os testes. Mostre um caso inválido e como a aplicação preserva os dados ou informa o erro.
