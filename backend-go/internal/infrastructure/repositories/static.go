package repositories

import (
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/domain"
)

type StaticFeeRepository struct{}

func NewStaticFeeRepository() domain.FeeRepository {
	return &StaticFeeRepository{}
}

func (r *StaticFeeRepository) GetBreakpoints(term int) []domain.Breakpoint {
	breakpoints, exists := FeeBreakpoints[term]
	if !exists {
		return []domain.Breakpoint{}
	}
	return breakpoints
}
