using System;
using Xunit;
using LoanFeeCalculator.Api.Domain;
using LoanFeeCalculator.Api.Infrastructure;
using LoanFeeCalculator.Api.Services;

namespace LoanFeeCalculator.Tests;

public class FeeCalculatorTests
{
    [Fact]
    public void RoundToMultipleOfFive_MathValidation()
    {
        Assert.Equal(115m, FeeMath.RoundToMultipleOfFive(2750m, 115.00m));
        Assert.Equal(50m, FeeMath.RoundToMultipleOfFive(1250m, 50.00m));
        Assert.Equal(54m, FeeMath.RoundToMultipleOfFive(1251m, 50.00m));
    }

    [Fact]
    public void CalculateFee_InterpolationValidation()
    {
        // 2750 over 24 months should return exactly $115
        var repo = new StaticFeeRepository();
        var strategy = new LinearInterpolationStrategy();
        var service = new FeeCalculatorService(repo, strategy);

        var application = new LoanApplication(2750m, 24);
        var fee = service.CalculateFee(application);

        Assert.Equal(115m, fee);
    }
}
