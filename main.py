import decode as RSD
import encode as RSE
from Vars import Variables


def main():
    V = Variables()
    prims = V.findPrimePoly()
    V.initTables(prims[0])
    print(bin(prims[0]))
    n = 15  # Длинна кода
    k = 5
    d = 2

    # t - число ошибок
    message = "hello"
    mesecc = RSE.rs_encode_msg([ord(x) for x in message], n - k, V)
    print("Original: %s" % mesecc)
    mesecc[5] = 63
    mesecc[11] = 63
    mesecc[12] = 63
    mesecc[4] = 63
    mesecc[4] = 63
    mesecc[3] = 63

    print("Corrupted: %s" % mesecc)

    corrected_message, corrected_ecc, pas = RSD.rs_correct_msg(mesecc, n - k, V,)
    print("Repaired: %s" % (corrected_message + corrected_ecc))
    print(''.join([chr(x) for x in corrected_message]))


if __name__ == "__main__":
    main()
