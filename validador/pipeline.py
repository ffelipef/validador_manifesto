from dataclasses import dataclass
from typing import Optional

from . import all_
from .util import Resultado
from . import ap

SIGMA = ap.SIGMA  # alfabeto de entrada da aplicação


@dataclass
class Fluxo:
    entrada: str
    status: str  # ACEITA | REJEITADA_AP | REJEITADA_ALL | ERRO_ALFABETO
    mensagem: str
    r_ap: Optional[Resultado] = None
    r_all: Optional[Resultado] = None
    cauda: str = ""

    @property
    def aceita(self):
        return self.status == "ACEITA"


def validar(entrada):
    fora = sorted(set(entrada) - SIGMA)
    if fora:
        return Fluxo(entrada, "ERRO_ALFABETO",
                     f"ERRO: símbolo(s) {fora} fora do alfabeto de entrada {''.join(sorted(SIGMA))}")
    r1 = ap.executar(entrada)
    if not r1.aceita:
        return Fluxo(entrada, "REJEITADA_AP", "REJEITADA: estrutura inválida (AP). ALL não executado.", r1)
    cauda = entrada.split("#", 1)[1]
    r2 = all_.executar(cauda)
    if not r2.aceita:
        return Fluxo(entrada, "REJEITADA_ALL", "REJEITADA: paletes x caixas != unidades (ALL).", r1, r2, cauda)
    return Fluxo(entrada, "ACEITA", "ACEITA: estrutura válida (AP) e unidades conferem (ALL).", r1, r2, cauda)
