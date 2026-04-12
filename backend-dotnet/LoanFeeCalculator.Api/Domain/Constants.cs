namespace LoanFeeCalculator.Api.Domain;

public static class Constants
{
    public const int Term12 = 12;
    public const int Term24 = 24;

    public static readonly int[] ValidTerms = { Term12, Term24 };

    public const decimal MinLoanAmount = 1000m;
    public const decimal MaxLoanAmount = 20000m;
    public const decimal FeeRoundingMultiple = 5m;
    public const decimal ZeroDecimal = 0m;
}
