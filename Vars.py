class Variables:
    def __init__(self, rootChar=2, degree=8, generator=2):
        self.rootChar = rootChar
        self.degree = degree
        self.generator = generator
        self.fieldChar = rootChar ** degree - 1
        self.gfExp = [0] * (256 * 2)
        self.gfLog = [0] * (256)

    def initTables(self, prim=0x11d):
        x = 1
        for i in range(self.fieldChar):
            self.gfExp[i] = x
            self.gfLog[x] = i
            x = self.__gf_mult_noLUT(x, self.generator, prim, self.fieldChar + 1)
        for i in range(self.fieldChar, self.fieldChar * 2):
            self.gfExp[i] = self.gfExp[i - self.fieldChar]

    def findPrimePoly(self):
        field_char_next = int(self.rootChar ** (self.degree + 1) - 1)
        prim_candidates = []
        correct_primes = []
        for i in range(self.fieldChar + 2, field_char_next, self.rootChar):
            prim_candidates.append(i)
        for prim in prim_candidates:
            seen = bytearray(self.fieldChar + 1)
            conflict = False

            x = 1
            for i in range(self.fieldChar):
                x = self.__gf_mult_noLUT(x, self.generator, prim, self.fieldChar + 1)

                if x > self.fieldChar or seen[x] == 1:
                    conflict = True
                    break
                else:
                    seen[x] = 1
            if not conflict:
                correct_primes.append(prim)

        return correct_primes

    @staticmethod
    def __gf_mult_noLUT(x, y, prim, field_charac_full):
        r = 0
        while y:
            if y & 1:
                r = r ^ x
            y = y >> 1
            x = x << 1
            if prim > 0 and x & field_charac_full:
                x = x ^ prim
        return r
