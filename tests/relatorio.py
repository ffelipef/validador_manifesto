"""Gera tests/RESULTADOS.md (entrada, esperado, obtido, regra). Uso: python -m tests.relatorio"""
from validador import all_, ap, pipeline

from .casos import ALL_CASOS, AP_CASOS, FLUXO_CASOS


def tabela(titulo, linhas):
    out = [f"## {titulo}", "", "| Entrada | Esperado | Obtido | Regra verificada | Resultado |", "|---|---|---|---|---|"]
    for e, esp, obt, regra in linhas:
        out.append(f"| `{e or 'ε'}` | {esp} | {obt} | {regra} | {'OK' if esp == obt else 'FALHA'} |")
    return "\n".join(out) + "\n"


def dec(b):
    return "ACEITA" if b else "REJEITA"


partes = [
    tabela("Módulo AP", [(e, dec(x), dec(ap.executar(e).aceita), r) for e, x, r in AP_CASOS]),
    tabela("Módulo ALL", [(e, dec(x), dec(all_.executar(e).aceita), r) for e, x, r in ALL_CASOS]),
    tabela("Fluxo completo", [(e, x, pipeline.validar(e).status, r) for e, x, r in FLUXO_CASOS]),
    "## Mensagem de erro (símbolo fora do alfabeto)\n\n```\n" + pipeline.validar("{[]}#PCX").mensagem + "\n```\n",
]
with open("tests/RESULTADOS.md", "w", encoding="utf-8") as f:
    f.write("# Resultados dos testes\n\n" + "\n".join(partes))
print("tests/RESULTADOS.md gerado")
