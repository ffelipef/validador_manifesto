def g(n, m, t):
    return "P" * n + "C" * m + "U" * t


# (entrada, aceita?, regra verificada)
AP_CASOS = [
    ("{[]}#PCU", True, "mínimo aceito: 1 contêiner, 1 volume vazio, cauda P+C+U+"),
    ("{[][]}#PPCCUUUU", True, "2 volumes irmãos"),
    ("{{[]}}#PCU", True, "contêiner dentro de contêiner"),
    ("{[[]]}#PCU", True, "volume dentro de volume"),
    ("{[]}{[]}#PCCUU", True, "2 contêineres no topo (B -> L B)"),
    ("{[][[]]}#PPPCUUU", True, "volumes irmãos, um aninhado"),
    ("{[]{[]}}#PCU", True, "volume e contêiner irmãos dentro de contêiner"),
    ("{{[]}{[]}}#PPCUU", True, "dois contêineres irmãos dentro de um"),
    ("{[[][]]}#PCUUUU", True, "volume com dois volumes"),
    ("{[]}{{[]}}#PCUUU", True, "topo com contêiner simples e aninhado"),
    ("", False, "caso-limite: entrada vazia"),
    ("{[]}#", False, "cauda ausente (exige P+C+U+)"),
    ("{[]#PCU", False, "contêiner não fechado"),
    ("{}#PCU", False, "contêiner vazio proibido"),
    ("{[}]#PCU", False, "fechamento cruzado { [ } ]"),
    ("[]#PCU", False, "volume no topo (só contêiner)"),
    ("{[{}]}#PCU", False, "contêiner dentro de volume proibido"),
    ("{[]}PCU", False, "falta o separador #"),
    ("{[]}#CPU", False, "cauda fora da ordem P,C,U"),
    ("{[]}#PC", False, "cauda sem U"),
    ("{[]}}#PCU", False, "fechamento em excesso"),
    ("{[]}#PCU#PCU", False, "segundo # não permitido"),
    ("#PCU", False, "sem estrutura antes do #"),
]

ALL_CASOS = [
    (g(1, 1, 1), True, "caso-limite aceito: 1x1=1"),
    (g(1, 2, 2), True, "1x2=2"), (g(2, 1, 2), True, "2x1=2"), (g(2, 2, 4), True, "2x2=4"),
    (g(1, 3, 3), True, "1x3=3"), (g(3, 1, 3), True, "3x1=3"), (g(3, 2, 6), True, "3x2=6"),
    (g(2, 3, 6), True, "2x3=6"), (g(4, 1, 4), True, "4x1=4"), (g(2, 4, 8), True, "2x4=8"),
    ("", False, "caso-limite: entrada vazia"),
    (g(1, 1, 2), False, "U em excesso (1x1 != 2)"),
    (g(2, 2, 3), False, "U insuficiente (2x2 != 3)"),
    (g(1, 2, 1), False, "U insuficiente (1x2 != 1)"),
    (g(2, 2, 5), False, "U em excesso (2x2 != 5)"),
    ("UCP", False, "ordem invertida"), ("PPUU", False, "sem bloco C"),
    ("CCUU", False, "sem bloco P"), ("PCPU", False, "blocos intercalados"),
    ("PCUC", False, "C após U"), ("P", False, "só P"), ("PC", False, "sem U"),
]

# (entrada, status esperado, regra)
FLUXO_CASOS = [
    ("{[][]}#PPCCUUUU", "ACEITA", "AP aceita e ALL aceita (2x2=4)"),
    ("{[}]#PPCCUUUU", "REJEITADA_AP", "AP rejeita (fechamento cruzado); ALL sem execução"),
    ("{[][]}#PPCCUUUUU", "REJEITADA_ALL", "AP aceita; ALL rejeita (2x2 != 5)"),
    ("{[]}#PCX", "ERRO_ALFABETO", "símbolo X fora do alfabeto de entrada"),
]
