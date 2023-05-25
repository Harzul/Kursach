import numpy as np


def content(V: np.array, sizeArray: list) -> str:
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
    return result


def getN(size: int) -> int:
    n = 8
    degree = 3
    if n - 1 > size:
        return n - 1
    else:
        while n < size or (n - size) < degree:
            n *= 2
            degree += 1
    return n - 1
