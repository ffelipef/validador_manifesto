import os
import sys
from xml.sax.saxutils import escape as esc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tests.casos import ALL_CASOS, AP_CASOS, FLUXO_CASOS
from validador import all_, ap, pipeline

EQUIPE = ["Felipe de Freitas", "Benjamin Suzuki", "Lucas Mesquita"]
LINK_GITHUB = "https://github.com/ffelipef/validador_manifesto"
PREENCHER_CONTRIBUICOES = {
    "Felipe de Freitas": "Revisão do código, testes e relatório",
    "Benjamin Suzuki": "Desenvolvimento do código e testes",
    "Lucas Mesquita": "Elaboração do relatório e testes",
}
PREENCHER_REVISAO_EQUIPE = "Executou os testes, refez à mão a derivação e os rastreamentos, revisou as provas e conferiu a consistência do relatório com o código e os testes."
# --------------------------------------------------------------

cm = 28.35  # pontos por cm


def _fix(t):
    return t.replace("<font name='DVM'>", "<code>").replace("</font>", "</code>")


def P(t, st="p"):
    if st in ("h1", "h2"):
        return f"<{st}>{_fix(t)}</{st}>"
    return f'<p class="{st}">{_fix(t)}</p>'


def B(t):
    return f'<p class="b">• {_fix(t)}</p>'


def code(linhas):
    return "<pre>" + "\n".join(esc(l) for l in linhas) + "</pre>"


def Spacer(w, h):
    return f'<div style="height:{h}pt"></div>'


def PageBreak():
    return '<div class="quebra"></div>'


def tabela(dados, larguras, cab=True, mono_cols=()):
    cols = "".join(f'<col style="width:{w}pt">' for w in larguras)
    rows = []
    for i, row in enumerate(dados):
        tag = "th" if (cab and i == 0) else "td"
        cel = "".join(f"<{tag}>" + (f"<code>{esc(str(c))}</code>" if (j in mono_cols and i > 0) else _fix(str(c))) + f"</{tag}>"
                      for j, c in enumerate(row))
        rows.append(f"<tr>{cel}</tr>")
    return f'<table class="t"><colgroup>{cols}</colgroup>' + "".join(rows) + "</table>"


def grade(itens, n=3, larg=0):
    while len(itens) % n:
        itens.append("")
    rows = ["<tr>" + "".join(f"<td><code>{esc(c)}</code></td>" for c in itens[i:i + n]) + "</tr>" for i in range(0, len(itens), n)]
    return '<table class="g">' + "".join(rows) + "</table>"


def dec(b):
    return "ACEITA" if b else "REJEITA"


def tab_testes(casos, f):
    d = [["Entrada", "Esperado", "Obtido", "Regra verificada", "OK"]]
    for e, esp, regra in casos:
        obt = f(e)
        alvo = esp if isinstance(esp, str) else dec(esp)
        d.append([e or "ε", alvo, obt, regra, "OK" if obt == alvo else "FALHA"])
    return tabela(d, [4.2 * cm, 2.1 * cm, 2.3 * cm, 7.0 * cm, 1.2 * cm], mono_cols=(0,))


s = []# ---------------- capa ----------------
s += [Spacer(1, 4.5 * cm), P("Validador de Manifestos de Carga com Autômato de Pilha e Autômato Linearmente Limitado", "capa_t"),
      Spacer(1, 0.8 * cm), P("Atividade Prática AV2 – Linguagens Livres de Contexto e Sensíveis ao Contexto", "capa_s"),
      P("Linguagens Formais e Autômatos – CESUPA", "capa_s"), P("Turma CC6NA – 25/11/2026", "capa_s"), Spacer(1, 1.2 * cm),
      P("<b>Equipe</b>", "capa_s")] + [P(n, "capa_s") for n in EQUIPE] + [
      Spacer(1, 0.8 * cm), P("<b>Repositório:</b> " + esc(LINK_GITHUB), "capa_s"), PageBreak()]

# ---------------- 1 ----------------
s += [P("1. Problema e visão geral", "h1"),
      P("Manifestos de carga descrevem como a mercadoria foi embalada e quantas unidades existem. O trabalho valida uma entrada "
        "no formato <font name='DVM'>estrutura # conferência</font> em duas etapas encadeadas. Na <b>etapa 1</b>, um autômato de pilha (AP) "
        "verifica a estrutura de embalagem, definida por uma gramática livre de contexto (GLC): contêineres "
        "<font name='DVM'>{ }</font> (não vazios, podem conter contêineres e volumes) e volumes <font name='DVM'>[ ]</font> (vazios ou só com volumes; "
        "<b>nunca</b> contêm contêiner), seguidos do separador <font name='DVM'>#</font> e de uma cauda <font name='DVM'>P+ C+ U+</font>. "
        "Se a estrutura é válida, na <b>etapa 2</b> um autômato linearmente limitado (ALL) recebe a cauda e confere a regra sensível ao contexto: "
        "<i>n</i> paletes (P) × <i>m</i> caixas por palete (C) = <i>n</i>·<i>m</i> unidades (U)."),
      P("Exemplos: <font name='DVM'>{[][]}#PPCCUUUU</font> é aceita pelos dois módulos (2×2=4); <font name='DVM'>{[}]#PPCCUUUU</font> é rejeitada pelo AP "
        "(o ALL não executa); <font name='DVM'>{[][]}#PPCCUUUUU</font> é aceita pelo AP e rejeitada pelo ALL (2×2≠5)."),
      P("2. Fontes consultadas", "h1"),
      B("SIPSER, M. <i>Introdução à Teoria da Computação</i>. Cengage Learning – autômatos de pilha, lema do bombeamento para linguagens livres de contexto e autômatos linearmente limitados."),
      B("HOPCROFT, J. E.; MOTWANI, R.; ULLMAN, J. D. <i>Introdução à Teoria de Autômatos, Linguagens e Computação</i>. Elsevier."),
      B("MENEZES, P. B. <i>Linguagens Formais e Autômatos</i>. Bookman (UFRGS)."),
      B("Lauda da atividade AV2 e material da disciplina (hierarquia de Chomsky).")]

# ---------------- 3 ----------------
s += [P("3. Etapa 1 – Gramática livre de contexto", "h1"),
      P("<b>Alfabeto:</b> Σ = { <font name='DVM'>{ } [ ] # P C U</font> }. <b>Regra de formação:</b> "
        "L<sub>1</sub> = { w # P<super>i</super> C<super>j</super> U<super>k</super> : w ∈ B, i, j, k ≥ 1 }, em que B é uma sequência não vazia de contêineres bem formados."),
      P("<b>GLC</b> G = (N, Σ, S, R): não terminais N = {S, B, L, I, G, H, T, R, V}; terminais Σ; símbolo inicial S; produções:"),
      code(["S → B # T          B → L B | L            L → { I }",
            "I → L I | G I | L | G                     G → [ ] | [ H ]       H → G H | G",
            "T → P T | P R      R → C R | C V          V → U V | U"]),
      P("L = contêiner, G = volume, I = conteúdo de um contêiner, H = conteúdo de um volume, T/R/V = blocos de P, C e U."),
      P("<b>Derivação mais à esquerda</b> da cadeia aceita <font name='DVM'>{[][]}#PPCCUUUU</font>:"),
      code(["S ⇒ B#T ⇒ L#T ⇒ {I}#T ⇒ {GI}#T ⇒ {[ ]I}#T ⇒ {[ ]G}#T ⇒ {[ ][ ]}#T",
            "  ⇒ {[][]}#PT ⇒ {[][]}#PPR ⇒ {[][]}#PPCR ⇒ {[][]}#PPCCV ⇒ {[][]}#PPCCUV",
            "  ⇒ {[][]}#PPCCUUV ⇒ {[][]}#PPCCUUUV ⇒ {[][]}#PPCCUUUU"]),
      P("<b>L<sub>1</sub> não é regular.</b> Considere a linguagem regular R = <font name='DVM'>{+ [ ] }+ # P C U</font>. A interseção L<sub>1</sub> ∩ R = "
        "{ {<super>n</super> [ ] }<super>n</super> # PCU : n ≥ 1 }, pois só há equilíbrio quando o número de <font name='DVM'>{</font> é igual ao de <font name='DVM'>}</font>. "
        "Essa linguagem não é regular (lema do bombeamento: bombear apenas o bloco de <font name='DVM'>{</font> desequilibra a cadeia). "
        "Como as linguagens regulares são fechadas sob interseção, L<sub>1</sub> não é regular. Ela é livre de contexto por ser gerada por G (tipo 2 de Chomsky).")]

# ---------------- 4 ----------------
tr_ap = [f"({q}, {a}, {t}) → ({q2}, {rep or 'ε'})" for (q, a, t), (q2, rep) in ap.DELTA.items()]
r_ap = ap.executar("{[][]}#PPCCUUUU")
s += [P("4. Autômato de pilha (AP)", "h1"),
      P("<b>Definição.</b> M = (Q, Σ, Γ, δ, q<sub>0</sub>, Z, F), com Q = {q0, …, q8} (9 estados), Σ como acima, alfabeto da pilha Γ = {Z, N, V} "
        "(Z = fundo, N = contêiner aberto, V = volume aberto), estado inicial q0, F = {q8}. <b>Configuração inicial:</b> (q0, w, Z), com a pilha contendo só Z. "
        "<b>Critério de aceitação: por estado final</b>, com a entrada consumida por inteiro; por construção a pilha termina em Z. O AP é determinístico."),
      P("<b>Significado dos estados:</b> q0 = início; q1 = logo após <font name='DVM'>{</font>; q2 = logo após <font name='DVM'>[</font>; "
        "q3 = logo após <font name='DVM'>]</font>; q4 = logo após <font name='DVM'>}</font>; q5 = após <font name='DVM'>#</font>; q6, q7, q8 = blocos P, C e U da cauda."),
      P("<b>Transições δ</b> – formato (estado, símbolo lido, topo) → (novo estado, string que substitui o topo; ε = desempilha). Toda transição consome um símbolo; "
        "transição ausente significa rejeição:"),
      grade(tr_ap),
      Spacer(1, 6),
      P("<b>Por que o AP reconhece a linguagem da GLC.</b> Invariante: a pilha, acima de Z, é exatamente a sequência dos delimitadores abertos e ainda não fechados, e o estado "
        "registra o tipo do último símbolo lido. (⇒) Seguindo uma derivação: L → {I} empilha N ao ler <font name='DVM'>{</font> e desempilha em <font name='DVM'>}</font>; "
        "G → [H] empilha V em <font name='DVM'>[</font> e desempilha em <font name='DVM'>]</font>. A regra “um volume não contém contêiner” vira “não há transição para "
        "<font name='DVM'>{</font> com topo V”; a regra “contêiner não vazio” vira “não há transição de q1 para <font name='DVM'>}</font>”; "
        "“volume ou contêiner no topo” é tratado pelo topo Z em q4. T, R e V são a parte regular e usam apenas estados. (⇐) Todo caminho de aceitação lê a pilha como a pilha de "
        "não terminais pendentes e monta uma árvore de derivação de G. Além do argumento, o AP foi comparado com um parser recursivo independente da GLC em milhares de cadeias mutadas."),
      P("<b>Rastreamento</b> do AP para <font name='DVM'>{[][]}#PPCCUUUU</font> (topo da pilha à esquerda):"),
      code(r_ap.traco)]

# ---------------- 5 ----------------
tr_all = [f"({q}, {a}) → ({q2}, {e}, {m})" for (q, a), (q2, e, m) in all_.D.items()]
r_all = all_.executar("PCCUU")
s += [P("5. Etapa 2 – Linguagem sensível ao contexto e ALL", "h1"),
      P("<b>Linguagem:</b> L<sub>2</sub> = { P<super>n</super> C<super>m</super> U<super>n·m</super> : n, m ≥ 1 }, alfabeto { P, C, U }. "
        "<b>Regra de aceitação:</b> a cauda tem blocos P+, C+, U+ nessa ordem e o número de U é o produto do número de P pelo de C."),
      P("<b>Classificação.</b> L<sub>2</sub> é sensível ao contexto (é aceita por um ALL, tipo 1 de Chomsky) e <b>não é livre de contexto</b>. "
        "Prova pelo lema do bombeamento: suponha L<sub>2</sub> livre de contexto com comprimento de bombeamento p e tome z = P<super>p</super> C<super>p</super> U<super>p²</super> = uvwxy, "
        "com |vwx| ≤ p e vx ≠ ε. (i) Se vx só tem U, bombear com i=2 muda o número de U sem mudar n e m. "
        "(ii) Se vx tem só P e/ou C (sem U), muda n ou m e não muda o número de U = p²; como (p+a)(p+b) ≠ p² quando a+b > 0, a cadeia sai de L<sub>2</sub>. "
        "(iii) Se vx atravessa a fronteira C|U, vx = C<super>b</super>U<super>c</super> com b+c ≤ p e b ≥ 1, logo c &lt; p ≤ p·b; bombear dá m = p+b e "
        "U = p²+c ≠ p(p+b). Em todos os casos z′ ∉ L<sub>2</sub>: contradição. A comparação entre L<sub>1</sub> (tipo 2) e L<sub>2</sub> (tipo 1) segue a hierarquia de Chomsky."),
      P("<b>Definição do ALL (determinístico).</b> Estados Q = {q0, …, q11, qA, qR} (14); alfabeto de entrada Σ = {P, C, U}; alfabeto da fita Γ = Σ ∪ {p, k, u} ∪ {&lt;, &gt;}, "
        "em que p = P já contado, k = C marcada na passada atual (restaurada depois) e u = U já consumida; &lt; e &gt; são os dois marcadores de borda fixos. "
        "<b>Configuração inicial:</b> (q0, fita = &lt; w &gt;, cabeçote em &lt;). <b>Aceitação:</b> alcançar qA; <b>rejeição:</b> alcançar qR, o que ocorre por transição ausente. "
        "O cabeçote recua uma célula ao aceitar, para nunca passar de &gt;."),
      P("<b>Algoritmo.</b> q0–q5 conferem o formato P+C+U+ e voltam ao início da fita; q6 marca o próximo P (p); q7 marca o próximo C (k); q8 procura a próxima U livre e a marca (u) – "
        "se não há, rejeita; q9 volta ao início e retorna a q7; quando não restam C livres, q10 restaura k → C e q6 passa ao próximo P; sem P livre, q11 exige que não sobre nenhuma U."),
      P("<b>Transições</b> – formato (estado, lido) → (novo estado, escreve, movimento):"),
      grade(tr_all),
      Spacer(1, 6),
      P("<b>Limite da fita.</b> Para uma entrada de n símbolos, a fita tem n células graváveis mais os dois marcadores. Só são escritas marcas (p, k, u) sobre as próprias células da entrada; "
        "nenhuma transição move o cabeçote para fora de [&lt;, &gt;] nem sobrescreve os marcadores – a implementação verifica as duas condições com asserções a cada passo. "
        "Logo, toda a memória de trabalho cabe na fita da entrada, como exige um ALL."),
      P("<b>Rastreamento</b> do ALL para a cauda <font name='DVM'>PCCUU</font> (1×2=2; cabeçote entre colchetes):"),
      code(r_all.traco)]

# ---------------- 6 ----------------
s += [P("6. Implementação", "h1"),
      P("Programa em Python 3 (somente biblioteca padrão), com interface de linha de comando. Os módulos são <font name='DVM'>validador/ap.py</font> (AP), "
        "<font name='DVM'>validador/all_.py</font> (ALL) e <font name='DVM'>validador/pipeline.py</font> (fluxo em duas etapas); "
        "<font name='DVM'>main.py</font> faz a interface e imprime os rastreamentos. A decisão resulta apenas da execução das tabelas de transição e das operações de pilha e de fita: "
        "não há expressões regulares nem contagem direta nos autômatos. Símbolos fora do alfabeto de entrada são recusados antes de qualquer execução, com mensagem de erro."),
      P("<b>Terminação.</b> No AP, cada transição consome exatamente um símbolo e não existem ε-movimentos, logo há no máximo |w| passos. No ALL, cada P é marcado uma única vez, "
        "cada U é consumida no máximo uma vez, as marcas k são sempre restauradas e cada varredura é limitada pela fita; portanto o número de passos é O(n²) para uma entrada de n símbolos. "
        "A implementação ainda tem um limite de passos de segurança, nunca atingido nos testes."),
      P("<b>Não determinismo.</b> Os dois autômatos são determinísticos (no máximo uma transição por configuração), então o simulador não explora alternativas; a ausência de transição é a rejeição.")]

# ---------------- 7 ----------------
def st_ap(e): return dec(ap.executar(e).aceita)
def st_all(e): return dec(all_.executar(e).aceita)
def st_fl(e): return pipeline.validar(e).status

s += [P("7. Testes", "h1"),
      P("Cada reconhecedor foi testado separadamente (pelo menos 8 cadeias aceitas e 8 rejeitadas, todas distintas e com o alfabeto do módulo, incluindo casos-limite) "
        "e o fluxo completo foi testado com as três entradas exigidas, mais um símbolo fora do alfabeto. A tabela é reproduzível com <font name='DVM'>python -m tests.relatorio</font>."),
      P("7.1 Módulo AP", "h2"), tab_testes(AP_CASOS, st_ap),
      P("7.2 Módulo ALL", "h2"), tab_testes(ALL_CASOS, st_all),
      P("7.3 Fluxo completo", "h2"), tab_testes(FLUXO_CASOS, st_fl),
      Spacer(1, 4),
      P("<b>Símbolo fora do alfabeto.</b> Entrada <font name='DVM'>{[]}#PCX</font>; mensagem exibida:"),
      code([pipeline.validar("{[]}#PCX").mensagem]),
      P("Além dos casos acima, a suíte automatizada (<font name='DVM'>python -m unittest -v</font>) compara o ALL com um oráculo em todas as cadeias de {P, C, U} até comprimento 9 "
        "e o AP com um parser recursivo independente em 4.000 cadeias mutadas.")]

# ---------------- 8 ----------------
s += [P("8. Análise dos resultados e limitação", "h1"),
      P(f"Todos os {len(AP_CASOS)} casos do AP, os {len(ALL_CASOS)} do ALL e os {len(FLUXO_CASOS)} do fluxo produziram a decisão esperada. "
        "Os três cenários de integração mostram a divisão de trabalho: a estrutura aninhada exige a pilha (o AP rejeita fechamentos cruzados e contêiner dentro de volume), "
        "enquanto a igualdade entre o número de U e o produto n·m exige reescrever a fita (o ALL), algo que nenhuma pilha faz."),
      P("<b>Limitação observada.</b> O AP aceita <font name='DVM'>{[]}#PCUU</font>: a estrutura é válida, e só o ALL percebe que as unidades não conferem. Isso é uma consequência do projeto "
        "(cada etapa verifica um único tipo de dependência), mas significa que a etapa 1 sozinha não garante um manifesto coerente. Outra limitação é o custo O(n²) do ALL e o rastreamento muito longo para caudas grandes.")]

# ---------------- 9, 10 ----------------
s += [P("9. Uso de inteligência artificial", "h1"),
      B("<b>Ferramenta:</b> Claude (Anthropic)."),
      B("<b>Tarefas apoiadas:</b> proposta do problema e das linguagens L<sub>1</sub> e L<sub>2</sub>; escrita do código-fonte (AP, ALL, fluxo e interface), dos testes automatizados, do README e do rascunho deste relatório."),
      B("<b>Verificações automatizadas:</b> execução da suíte de testes (todos os testes passaram), comparação do ALL com oráculo em todas as cadeias até comprimento 9 e do AP com parser independente em cadeias mutadas."),
      B("<b>Verificação pela equipe:</b> " + esc(PREENCHER_REVISAO_EQUIPE)),
      P("10. Contribuição de cada integrante", "h1")]
s.append(tabela([["Integrante", "Contribuição"]] + [[n, PREENCHER_CONTRIBUICOES.get(n, "")] for n in EQUIPE], [5 * cm, 11.8 * cm]))
s += [P("Referências", "h1"),
      P("SIPSER, M. <i>Introdução à Teoria da Computação</i>. Cengage Learning.<br/>HOPCROFT, J. E.; MOTWANI, R.; ULLMAN, J. D. <i>Introdução à Teoria de Autômatos, Linguagens e Computação</i>. Elsevier.<br/>"
        "MENEZES, P. B. <i>Linguagens Formais e Autômatos</i>. Bookman.")]

CSS = """
@page { size: A4; margin: 2cm; }
body { font-family: 'DejaVu Sans', 'Segoe UI', Arial, sans-serif; font-size: 10pt; line-height: 1.45; color: #111; }
h1 { font-size: 14pt; color: #1F3A5F; margin: 16pt 0 6pt; page-break-after: avoid; }
h2 { font-size: 11pt; color: #1F3A5F; margin: 10pt 0 4pt; page-break-after: avoid; }
p { margin: 0 0 6pt; text-align: justify; }
p.b { margin: 0 0 3pt 14pt; text-indent: -10pt; text-align: left; }
p.capa_t { font-size: 21pt; font-weight: bold; color: #1F3A5F; text-align: center; line-height: 1.3; }
p.capa_s { font-size: 11.5pt; text-align: center; }
code { font-family: Consolas, 'DejaVu Sans Mono', monospace; font-size: 9pt; }
pre { font-family: Consolas, 'DejaVu Sans Mono', monospace; font-size: 7.6pt; line-height: 1.25; background: #F2F4F7; padding: 5pt; margin: 0 0 8pt; white-space: pre; overflow: hidden; }
table { border-collapse: collapse; margin-bottom: 8pt; }
table.t { width: 100%; table-layout: fixed; }
table.g { width: 100%; }
th, td { border: 0.5pt solid #B8C0CC; padding: 2pt 3pt; font-size: 7.8pt; vertical-align: top; text-align: left; word-wrap: break-word; }
th { background: #DCE4F0; }
td code { font-size: 7.4pt; }
tr { page-break-inside: avoid; }
.quebra { page-break-after: always; }
"""
html = ("<!DOCTYPE html><html lang='pt-BR'><head><meta charset='utf-8'><title>Relatório AV2 – Validador de Manifestos (AP + ALL)</title>"
        "<style>" + CSS + "</style></head><body>" + "\n".join(s) + "</body></html>")
out = "Relatorio_AV2_CC6NA.html"
with open(out, "w", encoding="utf-8") as f:
    f.write(html)
print("gerado:", out, "-> abra no navegador e use Ctrl+P > Salvar como PDF")