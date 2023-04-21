import random

import numpy as np

import gf


class BCH(object):

    def __init__(self, n, t, size):
        q = n.bit_length()
        self.n = n
        self.t = t
        self.size = size
        if (n + 1).bit_length() <= q:
            raise ValueError("n != 2^q - 1")
        if t > (n - 1) // 2:
            raise ValueError("t > (n-1)/2")
        self.generateValues()

    def generateValues(self):
        poly = random.choice(self.findPrimePoly(self.n))
        self.pm = gf.gen_pow_matrix(
            poly)  # матрица соответствия между десятичным и степенным представлением в поле F^q_2

        self.R = self.pm[:(2 * self.t), 1]  # вектор из элементов поля F^q_2( нули кода)

        self.g = gf.minpoly(self.R, self.pm)[
            0]  # поиск минимального полинома в F_2[x] для набора корней, задаваемых R(порождающий многочлен кода, начиная со старшей степени)
        if (self.n - self.g.size + 1) < self.size:
            self.n = (self.n + 1) * 2 - 1
            self.generateValues()
            return
        print("Primitive polynomial: " + str(poly) + " ~ " + np.binary_repr(poly))
        print("Generator polynomial:", self.g)
        print("m (контрольные биты) = " + str(self.g.size - 1) + "\tk (предел размера сообщения) = " + str(
            self.n - self.g.size + 1))

    def findPrimePoly(self, n: int):
        field_char_next = (n + 1) * 2 - 1
        prim_candidates = []
        correct_primes = []
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

    def encode(self, U):
        k = U.shape[1]
        V = np.zeros((len(U), len(self.pm)), int)
        V[:, :k] = U
        for i in range(len(V)):
            V[i] = gf.polyadd(V[i], gf.polydiv(V[i], self.g, self.pm)[1])
        return V

    def decode(self, W):
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

    def dist(self, check=False):
        k = len(self.pm) - self.g.size + 1
        d = len(self.pm)
        u = np.arange(k - 1, -1, -1).reshape(1, -1)
        for i in range(2 ** k):
            v = self.encode((i >> u) & 1).reshape(-1)
            if check:
                r = gf.polydiv(v, self.g, self.pm)[1]
                if r.size != 1 or r[0] != 0:
                    return False
                s = gf.polyval(v, self.R, self.pm)
                for j in s:
                    if j != 0:
                        return False
            b = np.sum(v)
            if b < d and b != 0:
                d = b
        if check:
            return d >= self.R.size + 1
        else:
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
        return self.dist(check=True)

    @staticmethod
    def __gf_mult(x, y, prim, field_charac_full):
        r = 0
        while y:
            if y & 1:
                r = r ^ x
            y = y >> 1
            x = x << 1
            if prim > 0 and x & field_charac_full:
                x = x ^ prim
        return r


def content(V, sizeArray):
    index = 0
    ResultStr = []
    newPart = []
    for j in V[0]:
        if len(newPart) == sizeArray[index] - 1:
            newPart.append(str(j))
            ResultStr.append(newPart)
            newPart = []
            index += 1
            if index == len(sizeArray):
                break
            continue
        newPart.append(str(j))
    SplitedArr = []
    for i in range(len(ResultStr)):
        SplitedArr.append(''.join(ResultStr[i]))
    decoded = []
    for i in ResultStr:
        st = chr(int(''.join(i), 2))
        decoded.append(st)
    result = ''.join(decoded)
    print(result)


def getN(size):
    n = 8
    degree = 3
    if n - 1 > size:
        return n - 1
    else:
        while n < size or (n - size) < degree:
            n *= 2
            degree += 1
    return n - 1


if __name__ == "__main__":
    inputStr = "Привет, мир!"
    binaryStr = [format(ord(item), 'b') for item in inputStr]
    sizeArray = []
    for i in binaryStr:
        sizeArray.append(len(i))
    binaryStr = ''.join(format(ord(item), 'b') for item in inputStr)
    binaryInt = [int(x) for x in list(binaryStr)]

    t = 5
    n = getN(len(binaryInt))
    code = BCH(n, t, len(binaryInt))
    U = np.zeros((1, len(list(binaryInt))), int)
    U[0] = np.array(list(binaryInt))
    # U = np.random.randint(2, size=(1, 127))
    content(U, sizeArray)
    V = code.encode(U)

    W = V.copy()
    for w in W:
        w[random.sample(range(w.size), t)] ^= 1
    content(W, sizeArray)
    V1 = code.decode(W)
    content(V1, sizeArray)

