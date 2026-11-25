# Especificação formal

## 1. Problema
Manifesto de carga: `estrutura # conferência`. A estrutura descreve contêineres `{}` (podem conter contêineres e volumes) e volumes `[]` (só contêm volumes; **nunca** um contêiner). A conferência `P^n C^m U^k` informa n paletes, m caixas por palete e k unidades; o lote é válido se **k = n·m**.

## 2. GLC (etapa 1)
Alfabeto Σ = { `{`, `}`, `[`, `]`, `#`, `P`, `C`, `U` }. Regra de formação: L1 = { w # P^i C^j U^k : w ∈ B, i,j,k ≥ 1 }.
Não terminais: S, B, L, I, G, H, T, R, V · Início: S · Produções:
```
S → B # T          B → L B | L          L → { I }
I → L I | G I | L | G                   G → [ ] | [ H ]       H → G H | G
T → P T | P R      R → C R | C V        V → U V | U
```
**Derivação** de `{[][]}#PPPCCUUUUUU`:
S ⇒ B#T ⇒ L#T ⇒ {I}#T ⇒ {GI}#T ⇒ {[ ]I}#T ⇒ {[ ]G}#T ⇒ {[ ][ ]}#T ⇒ {[][]}#PT ⇒ {[][]}#PPT ⇒ {[][]}#PPPR ⇒ …#PPPCR ⇒ …#PPPCCV ⇒ …#PPPCCUV ⇒ …#PPPCCUUV ⇒ …#PPPCCUUUV ⇒ …#PPPCCUUUUV ⇒ …#PPPCCUUUUUV ⇒ {[][]}#PPPCCUUUUUU.

**L1 não é regular:** L1 ∩ `{+ [ ] }+ # P C U` = { {ⁿ [ ] }ⁿ # PCU : n ≥ 1 }, que não é regular (lema do bombeamento: bombear só `{` desequilibra). Regulares são fechadas sob interseção, logo L1 não é regular. É livre de contexto (gerada pela GLC) — Chomsky tipo 2.

## 3. AP (determinístico)
M = (Q, Σ, Γ, δ, q0, Z, F), Q = {q0…q8} (9 estados), Γ = {Z, N, V} (fundo, contêiner aberto, volume aberto), F = {q8}.
**Configuração inicial:** (q0, w, Z). **Aceitação: por estado final**, com entrada consumida por inteiro (a pilha termina em Z). Transições: ver `python main.py --tabelas` (fonte única, vem do código).

| Estado | Significado (último símbolo lido) | Regras |
|---|---|---|
| q0 | início | `{` (topo Z) → push N, q1 |
| q1 | após `{` | `{` → push N, q1 · `[` → push V, q2 (`}` aqui = contêiner vazio: rejeita) |
| q2 | após `[` | `[` → push V, q2 · `]` (topo V) → pop, q3 |
| q3 | após `]` | `[` (topo N ou V) → push V, q2 · `{` **só com topo N** → push N, q1 · `]` (topo V) → pop · `}` (topo N) → pop, q4 |
| q4 | após `}` | `{` (topo N ou Z) → push N, q1 · `[` (topo N) → push V, q2 · `}` (topo N) → pop · `#` (topo Z) → q5 |
| q5–q8 | cauda | `P` q5→q6, `P` q6→q6, `C` q6→q7, `C` q7→q7, `U` q7→q8, `U` q8→q8 (pilha intacta) |

**Por que AP = GLC.** Invariante: a pilha (acima de Z) é exatamente a sequência de delimitadores abertos e ainda não fechados, e o estado grava o tipo do último símbolo. (⇒) Por indução na derivação: L → {I} empilha N e desempilha no `}`; G → [H] empilha V e desempilha no `]`; a restrição “G não contém L” vira “`{` com topo V não tem transição”; “L/G não vazios” vira “`}` após `{` não tem transição” (q1). T/R/V são a parte regular, feita só com estados. (⇐) Todo caminho de aceitação gera uma árvore de derivação lendo a pilha como a pilha de não terminais pendentes. O código ainda é validado contra um parser recursivo independente da GLC (`tests/test_automatos.py`).

## 4. ALL (etapa 2)
Linguagem L2 = { P^n C^m U^(n·m) : n,m ≥ 1 }. Σ = {P,C,U}; Γ = Σ ∪ {p,k,u,<,>}; fita `<` w `>`: n células graváveis + 2 marcadores fixos; estados q0…q11, qA, qR (14). Transições em `all_.py` (`--tabelas`). Configuração inicial: (q0, cabeçote em `<`). Transição ausente = rejeita (qR); aceita em qA (o cabeçote recua 1 ao aceitar para nunca ultrapassar `>`).
Algoritmo: q0–q5 conferem o formato P⁺C⁺U⁺ e voltam a `<`; q6 marca o próximo P (p); q7 marca o próximo C (k); q8 consome a próxima U (u) — sem U livre ⇒ rejeita; q9 volta ao início; quando acabam os C, q10 restaura k→C e q6 pega o próximo P; sem P, q11 exige que não sobre U.
**Por que o limite da fita basta:** só se escrevem marcas (p,k,u) sobre as próprias células; nada é escrito fora de `<…>`, e uma asserção na execução checa que o cabeçote nunca sai nem sobrescreve os marcadores.
**Classificação:** L2 é sensível ao contexto (aceita por ALL, Chomsky tipo 1) e **não é livre de contexto**. Prova (bombeamento): seja z = P^p C^p U^(p²) = uvwxy, |vwx| ≤ p, vx ≠ ε. Se vx só tem U's, k muda e n·m não. Se tem P's e/ou C's mas não U's, n·m muda e k=p² não (ex.: (p+a)(p+b) ≠ p² se a+b>0). Se atravessa C|U, vx = C^b U^c com b+c ≤ p, logo c < p ≤ p·b: bombear (i=2) dá p(p+b) ≠ p²+c. Em todos os casos z′ ∉ L2. (Conferir com Sipser, *Introdução à Teoria da Computação*: lema do bombeamento p/ LLC e ALL.)

## 5. Terminação e não determinismo
- **AP:** cada transição consome 1 símbolo, não há ε-movimentos ⇒ ≤ |w| passos. **ALL:** cada P é marcado uma vez; cada U é consumida no máximo uma vez; as marcas k são sempre restauradas; cada varredura é limitada pela fita ⇒ O(n²) passos. Entradas com símbolo fora de Σ são recusadas antes, com mensagem de erro.
- **Ambos são determinísticos** (no máximo uma transição por configuração): não há exploração de alternativas; a ausência de transição é a rejeição.

## 6. Limitação observada nos testes (para comentar)
O AP aceita `{[][]}#PPPCCUUUUUUU` (a estrutura é válida) mesmo que as unidades não batam: a dependência só é vista pelo ALL, por design. Outra: o ALL faz O(n²) passos, e o rastreamento fica enorme para cauda longa.

## 7. Fontes e contribuições (preencher)
Fontes: _(livro-texto da disciplina, Sipser, Hopcroft/Ullman…)_ · Contribuição de cada integrante: _(…)_

## 8. Nota da lauda
Todas as cadeias selecionadas (módulos e fluxo) têm ≥ 18 caracteres; a exceção é a entrada vazia, caso-limite de cada módulo (verificado em `tests/test_automatos.py`).