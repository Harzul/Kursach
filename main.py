import random
import time

import numpy as np

from BCH import BCH
from support import getN, content


def correctCheck(A: np.ndarray, B: np.ndarray) -> bool:
    if np.array_equal(A, B):
        return True
    else:
        return False


def basicBCH() -> None:
    # inputStr = np.array([1, 1, 0, 0, 1])
    # binaryInt = inputStr
    inputStr = "Hello"
    binaryStr = [format(ord(item), 'b') for item in inputStr]
    sizeArray = []
    for i in binaryStr:
        sizeArray.append(len(i))
    binaryStr = ''.join(format(ord(item), 'b') for item in inputStr)
    binaryInt = [int(x) for x in list(binaryStr)]

    t = 2
    n = getN(len(binaryInt))

    code = BCH(n, t, len(binaryInt))
    U = np.zeros((1, len(list(binaryInt))), int)
    U[0] = np.array(list(binaryInt))
    print("Start message: {:s}".format(content(U, sizeArray)))
    V = code.encode(U)
    W = V.copy()
    for w in W:
        w[random.sample(range(w.size), t)] ^= 1
    print("Corrupted message: {:s}".format(content(W, sizeArray)))
    V1 = code.decodeE(W)
    print("Euclid decoding: {:s}".format(content(V1, sizeArray)))
    V2 = code.decodePGZ(W)
    print("PGZ decoding: {:s}".format(content(V2, sizeArray)))


def randomBCH(n=0, t=0) -> None:
    t = 2
    n = 15
    code = BCH(n, t, n, TEST=True)

    U = np.random.randint(2, size=(1, code.n - code.g.size + 1))
    V = code.encode(U)
    W = V.copy()
    for w in W:
        w[random.sample(range(w.size), t)] ^= 1
    V1 = code.decodeE(W)
    V2 = code.decodePGZ(W)

    print("Start message:\n{:s}".format(str(U)))


    print("Encoded message:\n{:s}".format(str(V)))
    print("Corrupted message: \n{:s}".format(str(W)))
    print("Euclid decoding:\n{:s}".format(str(V1)))
    print("PGZ decoding:\n{:s}".format(str(V2)))
#
# print("Encoded message == Corrupted message: {:s}".format(str(correctCheck(V, W))))
# print("Encoded message == Euclid decoded: {:s}".format(str(correctCheck(V, V1))))
# print("Encoded message == PGZ decoded: {:s}".format(str(correctCheck(V, V2))))


def createCompareTable() -> None:
    n = [7, 15, 31, 63, 127, 255, 511, 1023, 2047, 4095]
    t = [3, 7, 15, 31, 63, 127, 254, 508, 1016, 2032]

    for i in n:
        for j in t:
            if j * 2 > i:
                break
            print(i, j)
            code = BCH(i, j, i, TEST=True)
            U = np.random.randint(2, size=(75, code.n - code.g.size + 1))
            V = code.encode(U)
            W = V.copy()
            for w in W:
                w[random.sample(range(w.size), j + 1)] ^= 1
            t0 = time.time()
            V1 = code.decodeE(W)
            t1 = time.time()
            V2 = code.decodePGZ(W)
            t2 = time.time()

            e1 = np.sum(np.any(V != V1, axis=1)) / 75
            e2 = np.sum(np.any(V != V2, axis=1)) / 75
            d1 = np.sum([np.isnan(v) for v in V1[:, 0]]) / 75
            d2 = np.sum([np.isnan(v) for v in V2[:, 0]]) / 75

            # print("Euclid decode: {:.7f}".format((t1 - t0)/500))
            # print("PGZ decode: {:.7f}".format((t2 - t1)/500))
            # print("Encoded message == Euclid decoded: {:s}".format(str(correctCheck(V, V1))))
            # print("Encoded message == PGZ decoded: {:s}".format(str(correctCheck(V, V2))))
            # print("Euclid decoding problems: {:f}".format(sum([np.isnan(v) for v in V1[:, 0]])))
            # print("PGZ decoding problems: {:f}".format(sum([np.isnan(v) for v in V2[:, 0]])))
            print("PGZ OK: {:s}".format(str(1 - e1)))
            print("PGZ Miss: {:s}".format(str(e1 - d1)))
            print("PGZ Error: {:s}".format(str(d1)))
            print("Euclid OK: {:s}".format(str(1 - e2)))
            print("Euclid Miss: {:s}".format(str(e2 - d2)))
            print("Euclid Error: {:s}".format(str(d2)))


if __name__ == "__main__":
    # basicBCH()
    randomBCH()
    # createCompareTable()
