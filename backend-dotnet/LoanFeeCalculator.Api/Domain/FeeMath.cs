namespace LoanFeeCalculator.Api.Domain;

public static class FeeMath
{
    public static decimal RoundToMultipleOfFive(decimal loanAmount, decimal fee)
    {
        decimal total = loanAmount + fee;
        decimal remainder = total % Constants.FeeRoundingMultiple;
        
        if (remainder == Constants.ZeroDecimal)
        {
            return fee;
        }

        decimal adjustment = Constants.FeeRoundingMultiple - remainder;
        return fee + adjustment;
    }
}
