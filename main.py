"""Validador de manifestos em duas etapas (AP + ALL).
Uso: python main.py "{[][]}#PPPCCUUUUUU" [--trace] | python main.py --demo | python main.py --tabelas | python main.py
"""
import argparse

from validador import all_, ap, pipeline


def mostrar(f, trace):
    print(f"Entrada: {f.entrada!r}")
    if f.status == "ERRO_ALFABETO":
        print(f.mensagem + "\n")
        return
    print(f"[AP ] {'ACEITA ' if f.r_ap.aceita else 'REJEITA'} - {f.r_ap.motivo}")
    if trace:
        print("\n".join(f.r_ap.traco))
    if f.r_all is None:
        print("[ALL] não executado")
    else:
        print(f"[ALL] {'ACEITA ' if f.r_all.aceita else 'REJEITA'} (entrada do ALL: {f.cauda!r}) - {f.r_all.motivo}")
        if trace:
            print("\n".join(f.r_all.traco))
    print(f"=> {f.mensagem}\n")


def tabelas():
    print("AP: (estado, lido, topo) -> (novo estado, substitui topo por)")
    for k, v in ap.DELTA.items():
        print(f"  {k} -> {v[0]}, '{v[1]}'")
    print("\nALL: (estado, lido) -> (novo estado, escreve, move)")
    for k, v in all_.D.items():
        print(f"  {k} -> {v}")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("entrada", nargs="?")
    p.add_argument("--trace", action="store_true", help="mostra o rastreamento dos autômatos")
    p.add_argument("--demo", action="store_true", help="3 cenários de integração + símbolo inválido")
    p.add_argument("--arquivo", help="valida cada linha de um arquivo de entradas (ex.: exemplos/entradas.txt)")
    p.add_argument("--tabelas", action="store_true", help="imprime as funções de transição")
    a = p.parse_args()
    if a.tabelas:
        return tabelas()
    if a.demo:
        for e in ["{[][]}#PPPCCUUUUUU", "{[][}]}#PPPCCUUUUUU", "{[][]}#PPPCCUUUUUUU", "{[][]}#PPPCCUUUUUX"]:
            mostrar(pipeline.validar(e), True)
        return
    if a.arquivo:
        with open(a.arquivo, encoding="utf-8") as f:
            for linha in f:
                if linha.strip():
                    mostrar(pipeline.validar(linha.strip()), a.trace)
        return
    if a.entrada is not None:
        return mostrar(pipeline.validar(a.entrada), a.trace)
    print("Digite um manifesto (ou 'sair'). Alfabeto: { } [ ] # P C U")
    while True:
        try:
            s = input("entrada> ").strip()
        except EOFError:
            break
        if s == "sair":
            break
        mostrar(pipeline.validar(s), a.trace)


if __name__ == "__main__":
    main()