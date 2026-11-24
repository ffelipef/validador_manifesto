# Resultados dos testes

## Módulo AP

| Entrada | Esperado | Obtido | Regra verificada | Resultado |
|---|---|---|---|---|
| `{[]}#PCU` | ACEITA | ACEITA | mínimo aceito: 1 contêiner, 1 volume vazio, cauda P+C+U+ | OK |
| `{[][]}#PPCCUUUU` | ACEITA | ACEITA | 2 volumes irmãos | OK |
| `{{[]}}#PCU` | ACEITA | ACEITA | contêiner dentro de contêiner | OK |
| `{[[]]}#PCU` | ACEITA | ACEITA | volume dentro de volume | OK |
| `{[]}{[]}#PCCUU` | ACEITA | ACEITA | 2 contêineres no topo (B -> L B) | OK |
| `{[][[]]}#PPPCUUU` | ACEITA | ACEITA | volumes irmãos, um aninhado | OK |
| `{[]{[]}}#PCU` | ACEITA | ACEITA | volume e contêiner irmãos dentro de contêiner | OK |
| `{{[]}{[]}}#PPCUU` | ACEITA | ACEITA | dois contêineres irmãos dentro de um | OK |
| `{[[][]]}#PCUUUU` | ACEITA | ACEITA | volume com dois volumes | OK |
| `{[]}{{[]}}#PCUUU` | ACEITA | ACEITA | topo com contêiner simples e aninhado | OK |
| `ε` | REJEITA | REJEITA | caso-limite: entrada vazia | OK |
| `{[]}#` | REJEITA | REJEITA | cauda ausente (exige P+C+U+) | OK |
| `{[]#PCU` | REJEITA | REJEITA | contêiner não fechado | OK |
| `{}#PCU` | REJEITA | REJEITA | contêiner vazio proibido | OK |
| `{[}]#PCU` | REJEITA | REJEITA | fechamento cruzado { [ } ] | OK |
| `[]#PCU` | REJEITA | REJEITA | volume no topo (só contêiner) | OK |
| `{[{}]}#PCU` | REJEITA | REJEITA | contêiner dentro de volume proibido | OK |
| `{[]}PCU` | REJEITA | REJEITA | falta o separador # | OK |
| `{[]}#CPU` | REJEITA | REJEITA | cauda fora da ordem P,C,U | OK |
| `{[]}#PC` | REJEITA | REJEITA | cauda sem U | OK |
| `{[]}}#PCU` | REJEITA | REJEITA | fechamento em excesso | OK |
| `{[]}#PCU#PCU` | REJEITA | REJEITA | segundo # não permitido | OK |
| `#PCU` | REJEITA | REJEITA | sem estrutura antes do # | OK |

## Módulo ALL

| Entrada | Esperado | Obtido | Regra verificada | Resultado |
|---|---|---|---|---|
| `PCU` | ACEITA | ACEITA | caso-limite aceito: 1x1=1 | OK |
| `PCCUU` | ACEITA | ACEITA | 1x2=2 | OK |
| `PPCUU` | ACEITA | ACEITA | 2x1=2 | OK |
| `PPCCUUUU` | ACEITA | ACEITA | 2x2=4 | OK |
| `PCCCUUU` | ACEITA | ACEITA | 1x3=3 | OK |
| `PPPCUUU` | ACEITA | ACEITA | 3x1=3 | OK |
| `PPPCCUUUUUU` | ACEITA | ACEITA | 3x2=6 | OK |
| `PPCCCUUUUUU` | ACEITA | ACEITA | 2x3=6 | OK |
| `PPPPCUUUU` | ACEITA | ACEITA | 4x1=4 | OK |
| `PPCCCCUUUUUUUU` | ACEITA | ACEITA | 2x4=8 | OK |
| `ε` | REJEITA | REJEITA | caso-limite: entrada vazia | OK |
| `PCUU` | REJEITA | REJEITA | U em excesso (1x1 != 2) | OK |
| `PPCCUUU` | REJEITA | REJEITA | U insuficiente (2x2 != 3) | OK |
| `PCCU` | REJEITA | REJEITA | U insuficiente (1x2 != 1) | OK |
| `PPCCUUUUU` | REJEITA | REJEITA | U em excesso (2x2 != 5) | OK |
| `UCP` | REJEITA | REJEITA | ordem invertida | OK |
| `PPUU` | REJEITA | REJEITA | sem bloco C | OK |
| `CCUU` | REJEITA | REJEITA | sem bloco P | OK |
| `PCPU` | REJEITA | REJEITA | blocos intercalados | OK |
| `PCUC` | REJEITA | REJEITA | C após U | OK |
| `P` | REJEITA | REJEITA | só P | OK |
| `PC` | REJEITA | REJEITA | sem U | OK |

## Fluxo completo

| Entrada | Esperado | Obtido | Regra verificada | Resultado |
|---|---|---|---|---|
| `{[][]}#PPCCUUUU` | ACEITA | ACEITA | AP aceita e ALL aceita (2x2=4) | OK |
| `{[}]#PPCCUUUU` | REJEITADA_AP | REJEITADA_AP | AP rejeita (fechamento cruzado); ALL sem execução | OK |
| `{[][]}#PPCCUUUUU` | REJEITADA_ALL | REJEITADA_ALL | AP aceita; ALL rejeita (2x2 != 5) | OK |
| `{[]}#PCX` | ERRO_ALFABETO | ERRO_ALFABETO | símbolo X fora do alfabeto de entrada | OK |

## Mensagem de erro (símbolo fora do alfabeto)

```
ERRO: símbolo(s) ['X'] fora do alfabeto de entrada #CPU[]{}
```
