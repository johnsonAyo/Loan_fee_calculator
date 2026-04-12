package domain

import (
	"testing"

	"github.com/shopspring/decimal"
)

func TestRoundToMultipleOfFive(t *testing.T) {
	tests := []struct {
		amount   int64
		fee      string
		expected string
	}{
		{2750, "115.00", "115"},
		{1250, "50.00", "50"},
		{1251, "50.00", "54"},
	}

	for _, tt := range tests {
		amount := decimal.NewFromInt(tt.amount)
		fee, _ := decimal.NewFromString(tt.fee)
		expected, _ := decimal.NewFromString(tt.expected)

		result := RoundToMultipleOfFive(amount, fee)
		if !result.Equal(expected) {
			t.Errorf("amount %d fee %s: expected %s, got %s", tt.amount, tt.fee, expected, result)
		}
	}
}
