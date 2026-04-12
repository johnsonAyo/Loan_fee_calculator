using LoanFeeCalculator.Api.Domain;

namespace LoanFeeCalculator.Api.Infrastructure;

public class LinearInterpolationStrategy : IFeeInterpolationStrategy
{
    public decimal Calculate(decimal amount, Breakpoint lower, Breakpoint upper)
    {
        if (upper.LowerBound == lower.LowerBound)
        {
            throw new CalculationError("Invalid breakpoint data for interpolation: equal_breakpoint_amounts");
        }

        decimal x0 = lower.LowerBound;
        decimal y0 = lower.Fee;
        decimal x1 = upper.LowerBound;
        decimal y1 = upper.Fee;

        decimal fee = y0 + (amount - x0) * (y1 - y0) / (x1 - x0);
        return fee;
    }
}
