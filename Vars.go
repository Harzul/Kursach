package main

const (
	rootChar  = 2
	degree    = 8
	generator = 2
)

type GaluaFields struct {
	gfExp     []uint64
	gfLog     []uint64
	fieldChar uint64
}
type AlgosGF interface {
	Add(x, y uint64) uint64
	Sub(x, y uint64) uint64
	Mult(x, y uint64) uint64
	Div(x, y uint64) uint64
	Pow(x, y uint64) uint64
	Inverse(x, y uint64) uint64
	GfMultNoLUT(x, y, prime, fc uint64) uint64
	GfSetData(gfExp, gfLog []uint64, fieldChar uint64)
}

var GF AlgosGF = &GaluaFields{}
