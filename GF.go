package main

func (GF GaluaFields) Add(x, y int64) int64     { return x ^ y }
func (GF GaluaFields) Sub(x, y int64) int64     { return x ^ y }
func (GF GaluaFields) Mult(x, y int64) int64    { return -1 }
func (GF GaluaFields) Div(x, y int64) int64     { return -1 }
func (GF GaluaFields) Pow(x, y int64) int64     { return -1 }
func (GF GaluaFields) Inverse(x, y int64) int64 { return -1 }
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
