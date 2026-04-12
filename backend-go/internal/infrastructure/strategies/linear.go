package strategies

import (
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/domain"
	"github.com/shopspring/decimal"
)

type LinearInterpolationStrategy struct{}

func NewLinearInterpolationStrategy() domain.FeeInterpolationStrategy {
	return &LinearInterpolationStrategy{}
}

func (s *LinearInterpolationStrategy) Calculate(amount decimal.Decimal, lower domain.Breakpoint, upper domain.Breakpoint) (decimal.Decimal, error) {
	if upper.LowerBound.Equal(lower.LowerBound) {
		return decimal.Zero, &domain.CalculationError{
			Message: "Invalid breakpoint data for interpolation: equal_breakpoint_amounts",
		}
	}

	// fee = y0 + (amount - x0) * (y1 - y0) / (x1 - x0)
	x0 := lower.LowerBound
	y0 := lower.Fee
	x1 := upper.LowerBound
	y1 := upper.Fee

	amountMinusX0 := amount.Sub(x0)
	y1MinusY0 := y1.Sub(y0)
	x1MinusX0 := x1.Sub(x0)

	fee := y0.Add(amountMinusX0.Mul(y1MinusY0).Div(x1MinusX0))
	return fee, nil
}
