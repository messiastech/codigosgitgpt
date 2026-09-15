# Data Quality · contratos para CSV

Validador automatizado de dados com contrato JSON, relatório de erros por linha e saída adequada para pipelines.

## Executar em 2 minutos

Requer Python 3.11 ou superior. Usa apenas a biblioteca padrão: nenhuma dependência externa.
Abra o terminal na pasta deste projeto.

```sh
python app.py examples/customers.csv examples/contract.json
# Retorno 0 indica que todos os registros passaram
```

## Funcionalidades e decisões

- Regras: campos obrigatórios, unicidade, inteiros com mínimo e datas ISO.
- Relatório JSON inclui linha, campo e motivo, sem copiar valores pessoais.
- Retorno 0: válido; 1: violações; 2: erro de arquivo ou contrato.
- Contrato inválido é rejeitado antes de processar registros.
- Validação local em memória; unicidade considera espaços externos removidos.
- CSV vazio com cabeçalho é válido; use min_rows para exigir registros.

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

Contrato JSON → validação das regras → leitura CSV → validação por campo → relatório JSON + código de saída. Pode ser executado antes da carga de um pipeline.

## Demonstração em entrevista

Execute o exemplo, explique o fluxo acima e rode os testes. Mostre um caso inválido e como a aplicação preserva os dados ou informa o erro.
