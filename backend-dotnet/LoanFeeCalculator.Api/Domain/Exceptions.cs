using System;

namespace LoanFeeCalculator.Api.Domain;

public class LoanValidationError : Exception
{
    public LoanValidationError(string message) : base(message) { }
}

public class BreakpointNotFoundError : Exception
{
    public int Term { get; }
    public decimal Amount { get; }

    public BreakpointNotFoundError(string message, int term, decimal amount) : base(message)
    {
        Term = term;
        Amount = amount;
    }
}

public class CalculationError : Exception
{
    public CalculationError(string message) : base(message) { }
}
