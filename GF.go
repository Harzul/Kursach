package main

import "log"

func (GF GaluaFields) Add(x, y uint64) uint64 { return x ^ y }
func (GF GaluaFields) Sub(x, y uint64) uint64 { return x ^ y }
func (GF GaluaFields) Mult(x, y uint64) uint64 {
	if x == 0 || y == 0 {
		return 0
	}
	return GF.gfExp[(GF.gfLog[x]+GF.gfLog[y])%GF.fieldChar]
}
func (GF GaluaFields) Div(x, y uint64) uint64 {
	if y == 0 {
		log.Fatalln("Error, Dividing by zero")
	}
	if x == 0 {
		return 0
	}
	return GF.gfExp[(GF.gfLog[x]+GF.fieldChar-GF.gfLog[y])%GF.fieldChar]
}
func (GF GaluaFields) Pow(x, power uint64) uint64 {
	return GF.gfExp[(GF.gfLog[x]*power)%GF.fieldChar]
}
func (GF GaluaFields) Inverse(x uint64) uint64 {
	return GF.gfExp[GF.fieldChar-GF.gfLog[x]]
}
func (GF GaluaFields) GfMultNoLUT(x, y, prime, fc uint64) uint64 {
	var r uint64 = 0
	for y > 0 {
		if y%2 != 0 {
			r ^= x
		}
		y >>= 1
		x <<= 1
		if prime > 0 && x >= fc {
			x ^= prime
		}
	}
	return r
}

// Возможно стоит дописать через копирование чтобы не было пересечений как Btree
func (GF *GaluaFields) GfSetData(gfExp, gfLog []uint64, fieldChar uint64) {
	(*GF).gfExp = gfExp
	(*GF).gfLog = gfLog
	(*GF).fieldChar = fieldChar
}
