package domain

import (
	"github.com/shopspring/decimal"
)

const (
	Term12 = 12
	Term24 = 24
)

var (
	ValidTerms = []int{Term12, Term24}

	MinLoanAmount       = decimal.NewFromInt(1000)
	MaxLoanAmount       = decimal.NewFromInt(20000)
	FeeRoundingMultiple = decimal.NewFromInt(5)
	ZeroDecimal         = decimal.NewFromInt(0)
)
