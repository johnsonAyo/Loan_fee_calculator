package domain

import "github.com/shopspring/decimal"

type Breakpoint struct {
	LowerBound decimal.Decimal
	Fee        decimal.Decimal
}

type FeeRepository interface {
	GetBreakpoints(term int) []Breakpoint
}

type FeeInterpolationStrategy interface {
	Calculate(amount decimal.Decimal, lower Breakpoint, upper Breakpoint) (decimal.Decimal, error)
}
