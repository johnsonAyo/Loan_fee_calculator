using System.Collections.Generic;

namespace LoanFeeCalculator.Api.Domain;

public record Breakpoint(decimal LowerBound, decimal Fee);

public interface ILoanFeeRepository
{
    List<Breakpoint> GetBreakpoints(int term);
}

public interface IFeeInterpolationStrategy
{
    decimal Calculate(decimal amount, Breakpoint lower, Breakpoint upper);
}
