import encode as RSE
import decode as RSD
from Vars import Variables


def main():
    V = Variables()
    prims = V.findPrimePoly()
    V.initTables(prims[0])
    print(bin(prims[0]))
    n = 15 #Длинна кода
    k = 5
    d =3

    # t - число ошибок
    message = "hello"
    mesecc = RSE.rs_encode_msg([ord(x) for x in message], n - k, V)
    print("Original: %s" % mesecc)
    mesecc[1] = 63
    mesecc[2] = 63

    print("Corrupted: %s" % mesecc)

    corrected_message, corrected_ecc, pas = RSD.rs_correct_msg(mesecc, n - k, V, erase_pos=[0, 1, 2])
    print("Repaired: %s" % (corrected_message + corrected_ecc))
    print(''.join([chr(x) for x in corrected_message]))


if __name__ == "__main__":
    main()
