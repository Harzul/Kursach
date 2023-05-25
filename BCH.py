import random

import numpy as np

import gf


class BCH(object):

    def __init__(self, n, t, size, TEST=False):
        self.n = n
        self.t = t
        self.size = size
        if (n + 1).bit_length() <= n.bit_length():
            raise ValueError("n != 2^q - 1")
        if t > (n - 1) // 2:
            raise ValueError("t > (n-1)/2")
        self.generateValues(TEST)

    def generateValues(self, TEST=False) -> None:
        poly = random.choice(self.findPrimePoly(self.n))

        self.pm = gf.gen_pow_matrix(poly)
        # [0] = степень альфа при которой получается индекс массива от 1 до n-1
        # [1] = значение альфа при возведении ее в степень индекса от 1 до n-1
        self.R = self.pm[:(2 * self.t), 1]
        # вектор из элементов поля F^q_2( нули кода) первые :(2 * self.t) элементов по индексу 1

        self.g = gf.minpoly(self.R, self.pm)[0]
        # поиск минимального полинома в F_2[x] для набора корней, задаваемых R(порождающий многочлен кода, начиная со старшей степени)
        if not TEST:
            if (self.n - self.g.size + 1) < self.size:
                # Если избыточная часть не помещается увеличиваем n, чтобы получилось закодировать
                print("Can't create code for this n and t, increasing n...")
                self.n = (self.n + 1) * 2 - 1
                self.generateValues()
                return
        print("Примитивный многочлен: " + str(poly) + " ~ " + np.binary_repr(poly))
        print("Порождающий полином:", self.g)
        print("m (контрольные биты) = " + str(self.g.size - 1) + "\nk (предел размера сообщения) = " + str(
            self.n - self.g.size + 1))

    def findPrimePoly(self, n: int) -> list[int]:
        field_char_next = (n + 1) * 2 - 1
        correct_primes, prim_candidates = [], []

        for i in range(n + 2, field_char_next, 2):
            prim_candidates.append(i)
        for prim in prim_candidates:
            seen = [0] * (n + 1)
            conflict = False

            x = 1
            for i in range(n):
                x = self.__gf_mult(x, 2, prim, n + 1)

                if x > n or seen[x] == 1:
                    conflict = True
                    break
                else:
                    seen[x] = 1
            if not conflict:
                correct_primes.append(prim)

        return correct_primes

    # Систематическое кодирование циклического кода
    def encode(self, U: np.ndarray) -> np.ndarray:
        V = np.zeros((len(U), len(self.pm)), int)
        V[:, :U.shape[1]] = U  # Записываем U в V
        for i in range(len(V)):
            V[i] = gf.polyadd(V[i], gf.polydiv(V[i], self.g, self.pm)[1])
        return V

    def decodeE(self, W: np.ndarray) -> np.ndarray:
        V = W.astype(object)
        for i in range(len(V)):

            s = gf.polyval(V[i], self.R, self.pm)
            for j in s:
                if j != 0:
                    break
            else:
                continue

            S = np.append(s[::-1], [1])
            x = np.zeros(s.size + 2, int)
            x[0] = 1
            x = gf.euclid(x, S, self.pm, max_deg=s.size // 2)[2]
            e = x.size - 1

            x = gf.polyval(x, self.pm[:, 1], self.pm)
            x = self.pm[np.flatnonzero(x == 0), 1]

            if x.size != e:
                V[i, :] = np.nan
                continue

            x = self.pm[x - 1, 0] - 1
            V[i, x] = V[i, x] ^ 1

        return V

    def decodePGZ(self, W: np.ndarray) -> np.ndarray:
        V = W.astype(object)
        for i in range(len(V)):
            s = gf.polyval(V[i], self.R, self.pm)
            for j in s:
                if j != 0:
                    break
            else:
                continue
            e = s.size // 2
            while e > 0:
                S = np.empty((e, e), int)
                for j in range(e):
                    S[j] = s[j:j + e]
                x = gf.linsolve(S, s[e:2 * e], self.pm)
                if not np.any(np.isnan(x)):
                    break
                e -= 1
            else:
                V[i, :] = np.nan
                continue
            x = np.append(x, [1])
            x = gf.polyval(x, self.pm[:, 1], self.pm)
            x = self.pm[np.flatnonzero(x == 0), 1]
            x = self.pm[x - 1, 0] - 1
            V[i, x] = V[i, x] ^ 1
            s = gf.polyval(V[i], self.R, self.pm)
            for j in s:
                if j != 0:
                    V[i, :] = np.nan
                    break

        return V

    def dist(self):
        k = len(self.pm) - self.g.size + 1
        d = len(self.pm)
        u = np.arange(k - 1, -1, -1).reshape(1, -1)
        for i in range(2 ** k):
            v = self.encode((i >> u) & 1).reshape(-1)
            b = np.sum(v)
            if b < d and b != 0:
                d = b
        return d

    def checker(self):
        for i in self.g:
            if i != 0 and i != 1:
                return False
        a = np.zeros(len(self.pm) + 1, int)
        a[0] = a[-1] = 1
        a = gf.polydiv(a, self.g, self.pm)[1]
        if a.size != 1 or a[0] != 0:
            return False
        return self.dist()

    @staticmethod
    def __gf_mult(x: np.array, y: np.array, prim: int, field_charac_full: int):
        r = 0
        while y:
            if y & 1:
                r = r ^ x
            y = y >> 1  # y //2
            x = x << 1  # x * 2
            if prim > 0 and x & field_charac_full:
                x = x ^ prim
        return r
