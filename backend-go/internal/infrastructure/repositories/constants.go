package repositories

import (
	"github.com/johnsonafuye/fee-calculator-backend-go/internal/domain"
	"github.com/shopspring/decimal"
)

func newBreakpoint(amount int64, fee int64) domain.Breakpoint {
	return domain.Breakpoint{
		LowerBound: decimal.NewFromInt(amount),
		Fee:        decimal.NewFromInt(fee),
	}
}

var FeeBreakpoints = map[int][]domain.Breakpoint{
	domain.Term12: {
		newBreakpoint(1000, 50),
		newBreakpoint(2000, 90),
		newBreakpoint(3000, 90),
		newBreakpoint(4000, 115),
		newBreakpoint(5000, 100),
		newBreakpoint(6000, 120),
		newBreakpoint(7000, 140),
		newBreakpoint(8000, 160),
		newBreakpoint(9000, 180),
		newBreakpoint(10000, 200),
		newBreakpoint(11000, 220),
		newBreakpoint(12000, 240),
		newBreakpoint(13000, 260),
		newBreakpoint(14000, 280),
		newBreakpoint(15000, 300),
		newBreakpoint(16000, 320),
		newBreakpoint(17000, 340),
		newBreakpoint(18000, 360),
		newBreakpoint(19000, 380),
		newBreakpoint(20000, 400),
	},
	domain.Term24: {
		newBreakpoint(1000, 70),
		newBreakpoint(2000, 100),
		newBreakpoint(3000, 120),
		newBreakpoint(4000, 160),
		newBreakpoint(5000, 200),
		newBreakpoint(6000, 240),
		newBreakpoint(7000, 280),
		newBreakpoint(8000, 320),
		newBreakpoint(9000, 360),
		newBreakpoint(10000, 400),
		newBreakpoint(11000, 440),
		newBreakpoint(12000, 480),
		newBreakpoint(13000, 520),
		newBreakpoint(14000, 560),
		newBreakpoint(15000, 600),
		newBreakpoint(16000, 640),
		newBreakpoint(17000, 680),
		newBreakpoint(18000, 720),
		newBreakpoint(19000, 760),
		newBreakpoint(20000, 800),
	},
}
