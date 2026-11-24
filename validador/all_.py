"""Etapa 2 - Autômato Linearmente Limitado (ALL), determinístico.

Linguagem: { P^n C^m U^(n*m) : n, m >= 1 }  (n paletes x m caixas/palete = U unidades)
Fita: '<' w '>' (2 marcadores fixos + n células graváveis). O cabeçote nunca sai de [<, >]
e nunca sobrescreve os marcadores. Fita Γ = {P,C,U} + marcas {p,k,u} + {<,>}.
  p = P já contado | k = C marcada NESTA passada (restaurada depois) | u = U já consumida
Transição ausente = rejeição (qR). Aceita em qA.
"""
from .util import Resultado

SIGMA = set("PCU")
ESQ, DIR = "<", ">"
D = {}  # (estado, lido) -> (novo estado, escrito, movimento)


def t(q, lidos, q2, mov="R", esc=None):
    for a in lidos:
        D[(q, a)] = (q2, a if esc is None else esc, mov)


# --- fase 1: confere o formato P+ C+ U+ e volta ao início
t("q0", "<", "q1")
t("q1", "P", "q2")
t("q2", "P", "q2"); t("q2", "C", "q3")
t("q3", "C", "q3"); t("q3", "U", "q4")
t("q4", "U", "q4"); t("q4", ">", "q5", "L")
t("q5", "PCU", "q5", "L"); t("q5", "<", "q6")
# --- fase 2: para cada P, cada C consome exatamente 1 U
t("q6", "p", "q6"); t("q6", "P", "q7", esc="p"); t("q6", "C", "q11")   # q6: próximo P
t("q7", "Ppk", "q7"); t("q7", "C", "q8", esc="k"); t("q7", "Uu>", "q10", "L")  # q7: próximo C
t("q8", "Cku", "q8"); t("q8", "U", "q9", "L", esc="u")                 # q8: próximo U livre
t("q9", "PCUpku", "q9", "L"); t("q9", "<", "q7")                       # q9: volta ao início
t("q10", "k", "q10", "L", esc="C"); t("q10", "PCp", "q10", "L"); t("q10", "<", "q6")  # q10: restaura k->C
t("q11", "Cu", "q11"); t("q11", ">", "qA", "L")                             # q11: sobrou U? -> rejeita


def _linha(passo, q, cab, fita):
    vista = "".join(fita[:cab]) + "[" + fita[cab] + "]" + "".join(fita[cab + 1:])
    return f"{passo:>5} | {q:<4} | {cab:>3} | {vista}"


def executar(w):
    """Termina: cada U é consumida no máximo uma vez, cada P é marcado uma vez e as marcas
    k são sempre restauradas => O(n^2) passos. O limite abaixo é só uma rede de segurança."""
    fora = sorted(set(w) - SIGMA)
    if fora:
        raise ValueError(f"símbolo(s) fora do alfabeto do ALL {sorted(SIGMA)}: {fora}")
    fita = [ESQ] + list(w) + [DIR]
    q, cab, passo = "q0", 0, 0
    traco = ["passo | est. | cab | fita (cabeçote entre [ ])", _linha(0, q, cab, fita)]
    limite = 50 * len(fita) ** 3
    while q not in ("qA", "qR"):
        if passo > limite:
            raise RuntimeError("limite de passos excedido (não deveria ocorrer)")
        chave = (q, fita[cab])
        if chave not in D:
            q = "qR"
        else:
            q, esc, mov = D[chave]
            if fita[cab] in (ESQ, DIR):
                assert esc == fita[cab], "marcador de borda não pode ser sobrescrito"
            fita[cab] = esc
            cab += 1 if mov == "R" else -1
            assert 0 <= cab < len(fita), "cabeçote saiu da fita"
        passo += 1
        traco.append(_linha(passo, q, cab, fita))
    return Resultado(q == "qA", traco, "aceita em qA" if q == "qA" else "rejeita em qR")
