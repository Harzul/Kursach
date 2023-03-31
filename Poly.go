package main

import (
	"math"
)

func GetPrimes(number uint64) []uint64 {
	var result = make([]uint64, 0)
	var isPrime bool
	var i, j uint64 = 2, 2
	for ; i <= number; i++ {
		isPrime = true
		for ; j*j <= i; j++ {
			if i%j == 0 {
				isPrime = false
				break
			}
		}
		if isPrime {
			result = append(result, i)
		}
	}
	return result
}
func FindPrimePoly() []uint64 {
	var (
		fieldChar             = uint64(math.Pow(rootChar, degree) - 1)
		fieldCharNext         = uint64(math.Pow(rootChar, degree+1) - 1)
		primCandidates        = make([]uint64, 0)
		correctPrimes         = make([]uint64, 0)
		i              uint64 = 0
	)
	for i = fieldChar + 2; i < fieldCharNext; i += rootChar {
		primCandidates = append(primCandidates, i)
	}
	for _, prim := range primCandidates {
		var (
			seen                = make([]byte, fieldChar+1)
			conflictFlag        = false
			x            uint64 = 1
		)
		for i = 0; i < fieldChar; i++ {
			x = GF.GfMultNoLUT(x, generator, prim, fieldChar+1)
			if x > fieldChar || seen[x] == 1 {
				conflictFlag = true
				break
			} else {
				seen[x] = 1
			}
		}
		if !conflictFlag {
			correctPrimes = append(correctPrimes, prim)
		}
	}

	return correctPrimes
}
func InitTables(prim uint64) {
	var (
		fieldChar        = uint64(math.Pow(rootChar, degree) - 1)
		gfExp            = make([]uint64, fieldChar*2)
		gfLog            = make([]uint64, fieldChar+1)
		x         uint64 = 1
		i         uint64 = 0
	)
	for ; i < fieldChar; i++ {
		gfExp[i] = x
		gfLog[x] = i
		x = GF.GfMultNoLUT(x, generator, prim, fieldChar+1)
	}
	i = fieldChar
	for i = fieldChar; i < fieldChar*2; i++ {
		gfExp[i] = gfExp[i-fieldChar]
	}
	GF.GfSetData(gfExp, gfLog, fieldChar)

}
