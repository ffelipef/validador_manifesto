"""Etapa 1 - Autômato de Pilha determinístico (AP).

Linguagem: w # P+ C+ U+, com w gerada pela GLC de docs/ESPECIFICACAO.md
  { } = contêiner (não vazio; contém contêineres e/ou volumes)
  [ ] = volume    (vazio ou só com volumes; NUNCA contém contêiner)
Aceitação: por ESTADO FINAL (q8) com a entrada consumida por inteiro.
Pilha: Z (fundo), N (contêiner aberto), V (volume aberto). Topo = índice 0.
"""
from .util import Resultado

SIGMA = set("{}[]#PCU")
GAMMA = {"Z", "N", "V"}
INICIAL, FINAIS = "q0", {"q8"}
DELTA = {}  # (estado, lido, topo) -> (novo estado, string que SUBSTITUI o topo)


def _t(q, a, topo, q2, rep):
    DELTA[(q, a, topo)] = (q2, rep)


_t("q0", "{", "Z", "q1", "NZ")                 # 1º contêiner do topo
_t("q1", "{", "N", "q1", "NN")                 # logo após '{': contêiner aninhado
_t("q1", "[", "N", "q2", "VN")                 #                ou volume
_t("q2", "[", "V", "q2", "VV")                 # logo após '[': volume aninhado
_t("q2", "]", "V", "q3", "")                   #                ou fecha volume vazio
for _top in "NV":
    _t("q3", "[", _top, "q2", "V" + _top)      # após ']': novo volume (em N ou V)
_t("q3", "{", "N", "q1", "NN")                 #           novo contêiner (só em N!)
_t("q3", "]", "V", "q3", "")                   #           fecha volume
_t("q3", "}", "N", "q4", "")                   #           fecha contêiner
_t("q4", "{", "N", "q1", "NN")                 # após '}': contêiner irmão (dentro de N)
_t("q4", "{", "Z", "q1", "NZ")                 #           ou irmão no topo (pilha só Z)
_t("q4", "[", "N", "q2", "VN")                 #           volume irmão (só dentro de N)
_t("q4", "}", "N", "q4", "")                   #           fecha contêiner externo
_t("q4", "#", "Z", "q5", "Z")                  #           estrutura completa -> separador
_t("q5", "P", "Z", "q6", "Z")                  # cauda P+ C+ U+ (parte regular)
_t("q6", "P", "Z", "q6", "Z")
_t("q6", "C", "Z", "q7", "Z")
_t("q7", "C", "Z", "q7", "Z")
_t("q7", "U", "Z", "q8", "Z")
_t("q8", "U", "Z", "q8", "Z")


def executar(w):
    """Termina em <= |w| passos: toda transição consome 1 símbolo (sem ε-movimentos)
    e o AP é determinístico (no máximo 1 transição por configuração)."""
    q, pilha, i = INICIAL, "Z", 0
    traco = ["passo | estado | pos | lido | pilha (topo->fundo)",
             f"{0:>5} | {q:<6} | {i:>3} | {'-':<4} | {pilha}"]
    while i < len(w):
        chave = (q, w[i], pilha[0])
        if chave not in DELTA:
            return Resultado(False, traco,
                             f"sem transição para (estado={q}, lido={w[i]!r}, topo={pilha[0]}) na posição {i}")
        q, rep = DELTA[chave]
        pilha = rep + pilha[1:]
        i += 1
        traco.append(f"{i:>5} | {q:<6} | {i:>3} | {w[i-1]:<4} | {pilha}")
    if q in FINAIS and pilha == "Z":
        return Resultado(True, traco, f"entrada consumida; estado final {q}; pilha = Z")
    return Resultado(False, traco, f"entrada consumida, mas estado {q} não é final (pilha = {pilha})")
