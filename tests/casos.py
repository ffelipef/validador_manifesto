"""Casos de teste. Nota da lauda: as cadeias selecionadas têm no mínimo 18 caracteres
(a única exceção é a entrada vazia, usada como caso-limite)."""


def g(n, m, t):
    return "P" * n + "C" * m + "U" * t


# (entrada, aceita?, regra verificada)
AP_CASOS = [
    ("{[][]}#PPPCCUUUUUU", True, "caso-limite: aceita de comprimento mínimo (18)"),
    ("{{[]}}#PPPCCCUUUUUUU", True, "contêiner dentro de contêiner"),
    ("{[[]]}#PPPCCUUUUUUU", True, "volume dentro de volume"),
    ("{[]}{[]}#PPPCCUUUUUU", True, "2 contêineres no topo (B -> L B)"),
    ("{[][[]]}#PPPPCCUUUUUU", True, "volumes irmãos, um aninhado"),
    ("{[]{[]}}#PPPCCUUUUUU", True, "volume e contêiner irmãos dentro de contêiner"),
    ("{{[]}{[]}}#PPCCUUUUU", True, "dois contêineres irmãos dentro de um"),
    ("{[[][]]}#PCCCUUUUUUU", True, "volume com dois volumes"),
    ("{[]}{{[]}}#PPPCUUUUUU", True, "topo com contêiner simples e aninhado"),
    ("{[]}{[]}{[]}#PPCCUUUU", True, "3 contêineres no topo"),
    ("", False, "caso-limite: entrada vazia"),
    ("{[][]}{[][]}{[][]}#", False, "cauda ausente (exige P+C+U+)"),
    ("{[][][]#PPPCCUUUUUU", False, "contêiner não fechado"),
    ("{}{[]}#PPPCCUUUUUU", False, "contêiner vazio proibido"),
    ("{[][}]}#PPPCCUUUUUU", False, "fechamento cruzado"),
    ("[][][]#PPPCCUUUUUU", False, "volume no topo (só contêiner)"),
    ("{[{}][]}#PPPCCUUUUUU", False, "contêiner dentro de volume proibido"),
    ("{[][]}PPPCCUUUUUUU", False, "falta o separador #"),
    ("{[][]}#CCPPPUUUUUU", False, "cauda fora da ordem P,C,U"),
    ("{[][]}#PPPPPPPCCCCC", False, "cauda sem U"),
    ("{[][]}}#PPPCCUUUUUU", False, "fechamento em excesso"),
    ("{[][]}#PPPCC#UUUUUU", False, "segundo # não permitido"),
    ("#PPPCCUUUUUUUUUUUUU", False, "sem estrutura antes do #"),
]

ALL_CASOS = [
    (g(3, 4, 12), True, "caso-limite: aceita de comprimento mínimo (19): 3x4=12"),
    (g(4, 3, 12), True, "4x3=12"), (g(2, 6, 12), True, "2x6=12"), (g(6, 2, 12), True, "6x2=12"),
    (g(1, 9, 9), True, "1x9=9"), (g(9, 1, 9), True, "9x1=9"), (g(4, 4, 16), True, "4x4=16"),
    (g(2, 7, 14), True, "2x7=14"), (g(5, 3, 15), True, "5x3=15"), (g(3, 5, 15), True, "3x5=15"),
    ("", False, "caso-limite: entrada vazia"),
    (g(3, 4, 13), False, "U em excesso (3x4 != 13)"),
    (g(3, 4, 11), False, "U insuficiente (3x4 != 11)"),
    (g(4, 4, 15), False, "U insuficiente (4x4 != 15)"),
    (g(2, 6, 13), False, "U em excesso (2x6 != 13)"),
    (g(6, 2, 11), False, "U insuficiente (6x2 != 11)"),
    ("U" * 12 + "C" * 3 + "P" * 4, False, "ordem invertida"),
    ("P" * 4 + "U" * 16, False, "sem bloco C"),
    ("C" * 4 + "U" * 16, False, "sem bloco P"),
    ("P" * 3 + "C" * 3 + "P" * 3 + "U" * 9, False, "blocos intercalados"),
    ("P" * 3 + "C" * 4 + "U" * 12 + "C" * 2, False, "C após U"),
    ("P" * 18, False, "só P"),
    ("P" * 9 + "C" * 9, False, "sem U"),
]

# (entrada, status esperado, regra)
FLUXO_CASOS = [
    ("{[][]}#PPPCCUUUUUU", "ACEITA", "AP aceita e ALL aceita (3x2=6)"),
    ("{[][}]}#PPPCCUUUUUU", "REJEITADA_AP", "AP rejeita (fechamento cruzado); ALL sem execução"),
    ("{[][]}#PPPCCUUUUUUU", "REJEITADA_ALL", "AP aceita; ALL rejeita (3x2 != 7)"),
    ("{[][]}#PPPCCUUUUUX", "ERRO_ALFABETO", "símbolo X fora do alfabeto de entrada"),
]