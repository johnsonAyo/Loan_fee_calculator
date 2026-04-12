package domain



type LoanValidationError struct {
	Message string
}

func (e *LoanValidationError) Error() string {
	return e.Message
}

type BreakpointNotFoundError struct {
	Message string
	Term    int
	Amount  string
}

func (e *BreakpointNotFoundError) Error() string {
	return e.Message
}

type CalculationError struct {
	Message string
}

func (e *CalculationError) Error() string {
	return e.Message
}
