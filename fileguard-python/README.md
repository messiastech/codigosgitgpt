# FileGuard · integridade de arquivos

Cria um inventário SHA-256 e identifica arquivos alterados, adicionados e removidos.

## Executar em 2 minutos

Requer Python 3.11 ou superior. Usa apenas a biblioteca padrão: nenhuma dependência externa.
Abra o terminal na pasta deste projeto.

```sh
python app.py snapshot examples manifest.json
python app.py verify examples manifest.json
```

## Funcionalidades e decisões

- Leitura em blocos para limitar uso de memória.
- Comparação determinística com saída JSON e códigos de saída.
- Retorno 0: íntegro; 1: diferenças; 2: erro de execução.
- Ignora links simbólicos; inventário deve ficar fora da pasta monitorada.
- Detecta alterações acidentais; não substitui backup ou assinatura digital.
- Execute sobre uma pasta sem gravações simultâneas para obter um retrato consistente.

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

Pasta → leitura em blocos → SHA-256 por caminho relativo → inventário JSON. A verificação compara conjuntos de caminhos e hashes; nunca modifica os arquivos monitorados.

## Demonstração em entrevista

Execute o exemplo, explique o fluxo acima e rode os testes. Mostre um caso inválido e como a aplicação preserva os dados ou informa o erro.
