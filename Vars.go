package main

import "math"

const (
	rootChar  = 2
	degree    = 2
	generator = 2
)

var gfSize = int64(math.Pow(rootChar, degree))

type GaluaFields struct {
	gfExp     []byte
	gfLog     []byte
	fieldChar int64
}
type AlgosGF interface {
	Add(x, y int64) int64
	Sub(x, y int64) int64
	Mult(x, y int64) int64
	Div(x, y int64) int64
	Pow(x, y int64) int64
	Inverse(x, y int64) int64
	GfMultNoLUT(x, y, prime, fc uint64) uint64
}

var GF AlgosGF = GaluaFields{gfExp: make([]byte, gfSize*2), gfLog: make([]byte, gfSize), fieldChar: gfSize}
