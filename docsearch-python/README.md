# DocSearch · busca em documentos

Motor de busca local em arquivos Markdown e texto, com índice invertido e ranking TF-IDF.

## Executar em 2 minutos

Requer Python 3.11 ou superior. Usa apenas a biblioteca padrão: nenhuma dependência externa.
Abra o terminal na pasta deste projeto.

```sh
python app.py index examples --db search.db
python app.py search "python dados" --db search.db
```

## Funcionalidades e decisões

- Normaliza acentos e caixa; busca por união dos termos.
- Índice SQLite persistente com frequência dos termos.
- Reconstrução atômica: falhas preservam o índice anterior.
- Mostra pontuação e trecho inicial de cada resultado.
- Aceita .txt/.md UTF-8 até 2 MB; ignora links simbólicos.
- Não usa IA generativa e não lê PDF ou DOCX.

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

TXT/Markdown → normalização Unicode → frequências → índice invertido SQLite. Consultas combinam TF logarítmico e IDF suavizado; empates usam a ordem de indexação.

## Demonstração em entrevista

Execute o exemplo, explique o fluxo acima e rode os testes. Mostre um caso inválido e como a aplicação preserva os dados ou informa o erro.
