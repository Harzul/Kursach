def gfAdd(x, y):
    return x ^ y


def gfSub(x, y):
    return x ^ y


def gfNeg(x):
    return x


def gfInverse(x, V):
    return V.gfExp[V.fieldChar - V.gfLog[x]]


def gfMul(x, y, V):
    if x == 0 or y == 0:
        return 0
    return V.gfExp[(V.gfLog[x] + V.gfLog[y]) % V.fieldChar]


def gfDiv(x, y, V):
    if y == 0:
        raise ZeroDivisionError()
    if x == 0:
        return 0
    return V.gfExp[(V.gfLog[x] + V.fieldChar - V.gfLog[y]) % V.fieldChar]


def gfPow(x, power, V):
    return V.gfExp[(V.gfLog[x] * power) % V.fieldChar]
