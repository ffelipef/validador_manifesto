import random
import re
import unittest
from itertools import product

from validador import all_, ap, pipeline

from .casos import ALL_CASOS, AP_CASOS, FLUXO_CASOS


def oraculo_ap(w):
    """Parser recursivo descendente da GLC, independente do AP (validação cruzada)."""
    pos = 0

    def peek():
        return w[pos] if pos < len(w) else None

    def eat(c):
        nonlocal pos
        if peek() != c:
            raise ValueError
        pos += 1

    def V():
        eat("[")
        while peek() == "[":
            V()
        eat("]")

    def N():
        eat("{")
        n = 0
        while peek() in ("{", "["):
            N() if peek() == "{" else V()
            n += 1
        if n == 0:
            raise ValueError
        eat("}")

    try:
        N()
        while peek() == "{":
            N()
        eat("#")
        for s in "PCU":
            k = 0
            while peek() == s:
                pos += 1
                k += 1
            if k == 0:
                raise ValueError
        return pos == len(w)
    except ValueError:
        return False


def oraculo_all(w):
    m = re.fullmatch(r"(P+)(C+)(U+)", w)
    return bool(m) and len(m[1]) * len(m[2]) == len(m[3])


class TestRequisitos(unittest.TestCase):
    def test_quantidades_e_distincao(self):
        for casos in (AP_CASOS, ALL_CASOS):
            self.assertGreaterEqual(sum(c[1] for c in casos), 8)
            self.assertGreaterEqual(sum(not c[1] for c in casos), 8)
            self.assertEqual(len({c[0] for c in casos}), len(casos))

    def test_minimo_8_estados(self):
        est_ap = {k[0] for k in ap.DELTA} | {v[0] for v in ap.DELTA.values()}
        est_all = {k[0] for k in all_.D} | {v[0] for v in all_.D.values()}
        self.assertGreaterEqual(len(est_ap), 8)
        self.assertGreaterEqual(len(est_all), 8)


class TestModulos(unittest.TestCase):
    def test_ap(self):
        for e, esp, regra in AP_CASOS:
            with self.subTest(e=e):
                self.assertEqual(ap.executar(e).aceita, esp, regra)

    def test_all(self):
        for e, esp, regra in ALL_CASOS:
            with self.subTest(e=e):
                self.assertEqual(all_.executar(e).aceita, esp, regra)

    def test_fluxo(self):
        for e, esp, regra in FLUXO_CASOS:
            with self.subTest(e=e):
                self.assertEqual(pipeline.validar(e).status, esp, regra)

    def test_all_exaustivo_ate_9(self):
        for n in range(10):
            for tup in product("PCU", repeat=n):
                w = "".join(tup)
                self.assertEqual(all_.executar(w).aceita, oraculo_all(w), w)

    def test_ap_mutacoes_vs_oraculo(self):
        rnd = random.Random(0)
        base = [c[0] for c in AP_CASOS if c[1]]
        alfa = sorted(ap.SIGMA)
        for _ in range(4000):
            w = list(rnd.choice(base))
            for _ in range(rnd.randint(0, 3)):
                op, i = rnd.choice("ids"), rnd.randint(0, max(len(w) - 1, 0))
                if op == "i":
                    w.insert(i, rnd.choice(alfa))
                elif op == "d" and w:
                    del w[i]
                elif w:
                    w[i] = rnd.choice(alfa)
            w = "".join(w)
            self.assertEqual(ap.executar(w).aceita, oraculo_ap(w), w)


if __name__ == "__main__":
    unittest.main()
