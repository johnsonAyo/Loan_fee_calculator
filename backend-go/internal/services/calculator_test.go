package services

import (
	"testing"
	"github.com/shopspring/decimal"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/domain"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/infrastructure/repositories"
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/infrastructure/strategies"
)

func TestFeeCalculatorService_ExactBreakpoint(t *testing.T) {
	repo := repositories.NewStaticFeeRepository()
	strategy := strategies.NewLinearInterpolationStrategy()
	service := NewFeeCalculatorService(repo, strategy)

	app, _ := domain.NewLoanApplication(decimal.NewFromInt(3000), 12)
	fee, err := service.CalculateFee(app)

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	expected := decimal.NewFromInt(90)
	if !fee.Equal(expected) {
		t.Errorf("expected %v, got %v", expected, fee)
	}
}

func TestFeeCalculatorService_Interpolation(t *testing.T) {
	repo := repositories.NewStaticFeeRepository()
	strategy := strategies.NewLinearInterpolationStrategy()
	service := NewFeeCalculatorService(repo, strategy)

	app, _ := domain.NewLoanApplication(decimal.NewFromInt(2750), 24)
	fee, err := service.CalculateFee(app)

	if err != nil {
		t.Fatalf("expected no error, got %v", err)
	}

	// 2000 -> 100, 3000 -> 120
	// For 2750: fee is 100 + (2750-2000)*(120-100)/(3000-2000) = 100 + 750 * 20 / 1000 = 100 + 15 = 115
	// Total 2865 % 5 = 0. So fee 115.
	expected := decimal.NewFromInt(115)
	if !fee.Equal(expected) {
		t.Errorf("expected %v, got %v", expected, fee)
	}
}
