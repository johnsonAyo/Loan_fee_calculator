package domain

import (
	"fmt"
	"github.com/shopspring/decimal"
)

type LoanApplication struct {
	Amount decimal.Decimal
	Term   int
}

func NewLoanApplication(amount decimal.Decimal, term int) (*LoanApplication, error) {
	app := &LoanApplication{
		Amount: amount,
		Term:   term,
	}

	if err := app.Validate(); err != nil {
		return nil, err
	}

	return app, nil
}

func (a *LoanApplication) Validate() error {
	isValidTerm := false
	for _, t := range ValidTerms {
		if a.Term == t {
			isValidTerm = true
			break
		}
	}
	if !isValidTerm {
		return &LoanValidationError{Message: fmt.Sprintf("Invalid term %d. Must be one of %v", a.Term, ValidTerms)}
	}

	if a.Amount.LessThan(MinLoanAmount) || a.Amount.GreaterThan(MaxLoanAmount) {
		return &LoanValidationError{Message: fmt.Sprintf("Amount %v is outside allowed range %v-%v", a.Amount, MinLoanAmount, MaxLoanAmount)}
	}

	if a.Amount.Exponent() < -2 {
		return &LoanValidationError{Message: "Amount must have at most 2 decimal places"}
	}

	return nil
}
