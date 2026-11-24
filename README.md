# Validador de Manifestos de Carga (AP + ALL)

AV2 de Linguagens Formais e Autômatos (CESUPA). Valida uma entrada em duas etapas:
1. **AP** (autômato de pilha) confere a estrutura de embalagem: contêineres `{ }` e volumes `[ ]`, depois `#` e uma cauda `P+ C+ U+`.
2. **ALL** (autômato linearmente limitado) confere a regra sensível ao contexto: `P^n C^m U^(n·m)` (n paletes × m caixas por palete = U unidades).

Exemplos: `{[][]}#PPCCUUUU` (aceita) · `{[}]#PPCCUUUU` (AP rejeita) · `{[][]}#PPCCUUUUU` (ALL rejeita).

## Requisitos
Python 3.10+ (só biblioteca padrão, sem dependências).

## Comandos
```
python main.py "{[][]}#PPCCUUUU"            # decisão
python main.py "{[][]}#PPCCUUUU" --trace    # com rastreamento (pilha / fita)
python main.py --demo                       # 3 cenários de integração + símbolo inválido
python main.py --tabelas                    # funções de transição dos dois autômatos
python main.py                              # modo interativo
python -m unittest -v                       # testes
python -m tests.relatorio                   # gera tests/RESULTADOS.md (entrada/esperado/obtido/regra)
```

## Estrutura
`validador/ap.py` (AP) · `validador/all_.py` (ALL) · `validador/pipeline.py` (fluxo) · `tests/casos.py` (casos) · `docs/ESPECIFICACAO.md` (GLC, AP, ALL, provas)

## Uso de IA (preencher antes de entregar)
- Ferramenta: Claude (Anthropic)
- Tarefas apoiadas: _(ex.: rascunho do código, do README e da especificação)_
- O que a equipe verificou: _(ex.: executou os testes, refez à mão a derivação e os rastreamentos, revisou as provas)_
