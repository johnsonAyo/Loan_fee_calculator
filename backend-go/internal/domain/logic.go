package domain

import (
	"github.com/shopspring/decimal"
)

func RoundToMultipleOfFive(loanAmount decimal.Decimal, fee decimal.Decimal) decimal.Decimal {
	total := loanAmount.Add(fee)
	remainder := total.Mod(FeeRoundingMultiple)
	if remainder.Equal(ZeroDecimal) {
		return fee
	}
	adjustment := FeeRoundingMultiple.Sub(remainder)
	return fee.Add(adjustment)
}
