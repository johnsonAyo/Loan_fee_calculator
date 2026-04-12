using System;
using System.Linq;

namespace LoanFeeCalculator.Api.Domain;

public record LoanApplication
{
    public decimal Amount { get; init; }
    public int Term { get; init; }

    public LoanApplication(decimal amount, int term)
    {
        Amount = amount;
        Term = term;
        Validate();
    }

    private void Validate()
    {
        if (!Constants.ValidTerms.Contains(Term))
        {
            throw new LoanValidationError($"Invalid term {Term}. Must be one of [{string.Join(", ", Constants.ValidTerms)}]");
        }

        if (Amount < Constants.MinLoanAmount || Amount > Constants.MaxLoanAmount)
        {
            throw new LoanValidationError($"Amount {Amount} is outside allowed range {Constants.MinLoanAmount}-{Constants.MaxLoanAmount}");
        }

        // Check decimal places (must be at most 2)
        decimal amountMultiplier = Amount * 100;
        if (amountMultiplier != Math.Truncate(amountMultiplier))
        {
            throw new LoanValidationError("Amount must have at most 2 decimal places");
        }
    }
}
