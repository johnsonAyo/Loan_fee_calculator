package services

import (
	"fmt"
	"sort"

	"github.com/johnsonafuye/fee-calculator-backend-go/internal/domain"
	"github.com/shopspring/decimal"
)

type FeeCalculatorService struct {
	repository domain.FeeRepository
	strategy   domain.FeeInterpolationStrategy
}

func NewFeeCalculatorService(repo domain.FeeRepository, strategy domain.FeeInterpolationStrategy) *FeeCalculatorService {
	return &FeeCalculatorService{
		repository: repo,
		strategy:   strategy,
	}
}

func (s *FeeCalculatorService) CalculateFee(application *domain.LoanApplication) (decimal.Decimal, error) {
	breakpoints := s.repository.GetBreakpoints(application.Term)

	// In Go, since we use static slices, they are already sorted, but we reproduce the same robust check for safety.
	isSorted := true
	for i := 0; i < len(breakpoints)-1; i++ {
		if breakpoints[i].LowerBound.GreaterThan(breakpoints[i+1].LowerBound) {
			isSorted = false
			break
		}
	}
	if !isSorted {
		sort.Slice(breakpoints, func(i, j int) bool {
			return breakpoints[i].LowerBound.LessThan(breakpoints[j].LowerBound)
		})
	}

	amounts := make([]decimal.Decimal, len(breakpoints))
	for i, bp := range breakpoints {
		amounts[i] = bp.LowerBound
	}

	// bisect_left equivalent
	position := sort.Search(len(amounts), func(i int) bool {
		return amounts[i].GreaterThanOrEqual(application.Amount)
	})

	if position >= len(breakpoints) || (position == 0 && !amounts[position].Equal(application.Amount)) {
		return decimal.Zero, &domain.BreakpointNotFoundError{
			Message: fmt.Sprintf("Unable to find fee breakpoints for term=%d amount=%v", application.Term, application.Amount),
			Term:    application.Term,
			Amount:  application.Amount.String(),
		}
	}

	if amounts[position].Equal(application.Amount) {
		roundedFee := domain.RoundToMultipleOfFive(application.Amount, breakpoints[position].Fee)
		return roundedFee, nil
	}

	lower := breakpoints[position-1]
	upper := breakpoints[position]

	baseFee, err := s.strategy.Calculate(application.Amount, lower, upper)
	if err != nil {
		return decimal.Zero, err
	}

	roundedFee := domain.RoundToMultipleOfFive(application.Amount, baseFee)
	return roundedFee, nil
}
