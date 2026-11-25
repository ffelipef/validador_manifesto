# Resultados dos testes

## Módulo AP

| Entrada | Esperado | Obtido | Regra verificada | Resultado |
|---|---|---|---|---|
| `{[][]}#PPPCCUUUUUU` | ACEITA | ACEITA | caso-limite: aceita de comprimento mínimo (18) | OK |
| `{{[]}}#PPPCCCUUUUUUU` | ACEITA | ACEITA | contêiner dentro de contêiner | OK |
| `{[[]]}#PPPCCUUUUUUU` | ACEITA | ACEITA | volume dentro de volume | OK |
| `{[]}{[]}#PPPCCUUUUUU` | ACEITA | ACEITA | 2 contêineres no topo (B -> L B) | OK |
| `{[][[]]}#PPPPCCUUUUUU` | ACEITA | ACEITA | volumes irmãos, um aninhado | OK |
| `{[]{[]}}#PPPCCUUUUUU` | ACEITA | ACEITA | volume e contêiner irmãos dentro de contêiner | OK |
| `{{[]}{[]}}#PPCCUUUUU` | ACEITA | ACEITA | dois contêineres irmãos dentro de um | OK |
| `{[[][]]}#PCCCUUUUUUU` | ACEITA | ACEITA | volume com dois volumes | OK |
| `{[]}{{[]}}#PPPCUUUUUU` | ACEITA | ACEITA | topo com contêiner simples e aninhado | OK |
| `{[]}{[]}{[]}#PPCCUUUU` | ACEITA | ACEITA | 3 contêineres no topo | OK |
| `ε` | REJEITA | REJEITA | caso-limite: entrada vazia | OK |
| `{[][]}{[][]}{[][]}#` | REJEITA | REJEITA | cauda ausente (exige P+C+U+) | OK |
| `{[][][]#PPPCCUUUUUU` | REJEITA | REJEITA | contêiner não fechado | OK |
| `{}{[]}#PPPCCUUUUUU` | REJEITA | REJEITA | contêiner vazio proibido | OK |
| `{[][}]}#PPPCCUUUUUU` | REJEITA | REJEITA | fechamento cruzado | OK |
| `[][][]#PPPCCUUUUUU` | REJEITA | REJEITA | volume no topo (só contêiner) | OK |
| `{[{}][]}#PPPCCUUUUUU` | REJEITA | REJEITA | contêiner dentro de volume proibido | OK |
| `{[][]}PPPCCUUUUUUU` | REJEITA | REJEITA | falta o separador # | OK |
| `{[][]}#CCPPPUUUUUU` | REJEITA | REJEITA | cauda fora da ordem P,C,U | OK |
| `{[][]}#PPPPPPPCCCCC` | REJEITA | REJEITA | cauda sem U | OK |
| `{[][]}}#PPPCCUUUUUU` | REJEITA | REJEITA | fechamento em excesso | OK |
| `{[][]}#PPPCC#UUUUUU` | REJEITA | REJEITA | segundo # não permitido | OK |
| `#PPPCCUUUUUUUUUUUUU` | REJEITA | REJEITA | sem estrutura antes do # | OK |

## Módulo ALL

| Entrada | Esperado | Obtido | Regra verificada | Resultado |
|---|---|---|---|---|
| `PPPCCCCUUUUUUUUUUUU` | ACEITA | ACEITA | caso-limite: aceita de comprimento mínimo (19): 3x4=12 | OK |
| `PPPPCCCUUUUUUUUUUUU` | ACEITA | ACEITA | 4x3=12 | OK |
| `PPCCCCCCUUUUUUUUUUUU` | ACEITA | ACEITA | 2x6=12 | OK |
| `PPPPPPCCUUUUUUUUUUUU` | ACEITA | ACEITA | 6x2=12 | OK |
| `PCCCCCCCCCUUUUUUUUU` | ACEITA | ACEITA | 1x9=9 | OK |
| `PPPPPPPPPCUUUUUUUUU` | ACEITA | ACEITA | 9x1=9 | OK |
| `PPPPCCCCUUUUUUUUUUUUUUUU` | ACEITA | ACEITA | 4x4=16 | OK |
| `PPCCCCCCCUUUUUUUUUUUUUU` | ACEITA | ACEITA | 2x7=14 | OK |
| `PPPPPCCCUUUUUUUUUUUUUUU` | ACEITA | ACEITA | 5x3=15 | OK |
| `PPPCCCCCUUUUUUUUUUUUUUU` | ACEITA | ACEITA | 3x5=15 | OK |
| `ε` | REJEITA | REJEITA | caso-limite: entrada vazia | OK |
| `PPPCCCCUUUUUUUUUUUUU` | REJEITA | REJEITA | U em excesso (3x4 != 13) | OK |
| `PPPCCCCUUUUUUUUUUU` | REJEITA | REJEITA | U insuficiente (3x4 != 11) | OK |
| `PPPPCCCCUUUUUUUUUUUUUUU` | REJEITA | REJEITA | U insuficiente (4x4 != 15) | OK |
| `PPCCCCCCUUUUUUUUUUUUU` | REJEITA | REJEITA | U em excesso (2x6 != 13) | OK |
| `PPPPPPCCUUUUUUUUUUU` | REJEITA | REJEITA | U insuficiente (6x2 != 11) | OK |
| `UUUUUUUUUUUUCCCPPPP` | REJEITA | REJEITA | ordem invertida | OK |
| `PPPPUUUUUUUUUUUUUUUU` | REJEITA | REJEITA | sem bloco C | OK |
| `CCCCUUUUUUUUUUUUUUUU` | REJEITA | REJEITA | sem bloco P | OK |
| `PPPCCCPPPUUUUUUUUU` | REJEITA | REJEITA | blocos intercalados | OK |
| `PPPCCCCUUUUUUUUUUUUCC` | REJEITA | REJEITA | C após U | OK |
| `PPPPPPPPPPPPPPPPPP` | REJEITA | REJEITA | só P | OK |
| `PPPPPPPPPCCCCCCCCC` | REJEITA | REJEITA | sem U | OK |

## Fluxo completo

| Entrada | Esperado | Obtido | Regra verificada | Resultado |
|---|---|---|---|---|
| `{[][]}#PPPCCUUUUUU` | ACEITA | ACEITA | AP aceita e ALL aceita (3x2=6) | OK |
| `{[][}]}#PPPCCUUUUUU` | REJEITADA_AP | REJEITADA_AP | AP rejeita (fechamento cruzado); ALL sem execução | OK |
| `{[][]}#PPPCCUUUUUUU` | REJEITADA_ALL | REJEITADA_ALL | AP aceita; ALL rejeita (3x2 != 7) | OK |
| `{[][]}#PPPCCUUUUUX` | ERRO_ALFABETO | ERRO_ALFABETO | símbolo X fora do alfabeto de entrada | OK |

## Mensagem de erro (símbolo fora do alfabeto)

```
ERRO: símbolo(s) ['X'] fora do alfabeto de entrada #CPU[]{}
```