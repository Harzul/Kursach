import gfBasicMath as GFM


def gfPolyScale(p, x, V):
    out = [0] * len(p)
    for i in range(len(p)):
        out[i] = GFM.gfMul(p[i], x, V)
    return out


def gfPolyAdd(p, q):
    q_len = len(q)
    r = [0] * max(len(p), q_len)
    r[len(r) - len(p):len(r)] = p
    for i in range(q_len):
        r[i + len(r) - q_len] ^= q[i]
    return r


def gfPolyMul(p, q, V):
    r = [0] * (len(p) + len(q) - 1)
    lp = [V.gfLog[p[i]] for i in range(len(p))]
    for j in range(len(q)):
        qj = q[j]
        if qj != 0:
            lq = V.gfLog[qj]
            for i in range(len(p)):
                if p[i] != 0:
                    r[i + j] ^= V.gfExp[lp[i] + lq]
    return r


def gfPolyNeg(poly):
    return poly


def gfPolyDiv(dividend, divisor, V):
    msg_out = [0] * dividend
    divisor_len = len(divisor)
    for i in range(len(dividend) - (divisor_len - 1)):
        coef = msg_out[i]
        if coef != 0:
            for j in range(1, divisor_len):
                if divisor[j] != 0:
                    msg_out[i + j] ^= GFM.gfMul(divisor[j], coef, V)
    separator = -(divisor_len - 1)
    return msg_out[:separator], msg_out[separator:]


def gfPolySquare(poly, V):
    length = len(poly)
    out = bytearray(2 * length - 1)
    for i in range(length - 1):
        p = poly[i]
        k = 2 * i
        if p != 0:
            out[k] = V.gfExp[2 * V.gfLog[p]]
    out[2 * length - 2] = V.gfExp[2 * V.gfLog[poly[length - 1]]]
    if out[0] == 0: out[0] = 2 * poly[1] - 1
    return out


def gfPolyEval(poly, x, V):
    y = poly[0]
    for i in range(1, len(poly)):
        y = GFM.gfMul(y, x, V) ^ poly[i]
    return y
