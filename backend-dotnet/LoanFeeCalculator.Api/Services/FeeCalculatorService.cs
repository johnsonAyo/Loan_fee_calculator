using System.Collections.Generic;
using System.Linq;
using LoanFeeCalculator.Api.Domain;

namespace LoanFeeCalculator.Api.Services;

public interface IFeeCalculatorService
{
    decimal CalculateFee(LoanApplication application);
}

public class FeeCalculatorService : IFeeCalculatorService
{
    private readonly ILoanFeeRepository _repository;
    private readonly IFeeInterpolationStrategy _strategy;

    public FeeCalculatorService(ILoanFeeRepository repository, IFeeInterpolationStrategy strategy)
    {
        _repository = repository;
        _strategy = strategy;
    }

    public decimal CalculateFee(LoanApplication application)
    {
        var breakpoints = _repository.GetBreakpoints(application.Term);

        // Sort safety measure
        var isSorted = true;
        for (int i = 0; i < breakpoints.Count - 1; i++)
        {
            if (breakpoints[i].LowerBound > breakpoints[i + 1].LowerBound)
            {
                isSorted = false; break;
            }
        }
        if (!isSorted) breakpoints = breakpoints.OrderBy(b => b.LowerBound).ToList();

        var amounts = breakpoints.Select(b => b.LowerBound).ToList();
        
        // Exact equivalent of bisect_left
        int position = BinarySearchLeft(amounts, application.Amount);

        if (position >= breakpoints.Count || (position == 0 && amounts[position] != application.Amount))
        {
            throw new BreakpointNotFoundError(
                $"Unable to find fee breakpoints for term={application.Term} amount={application.Amount}",
                application.Term, application.Amount);
        }

        if (amounts[position] == application.Amount)
        {
            return FeeMath.RoundToMultipleOfFive(application.Amount, breakpoints[position].Fee);
        }

        var lower = breakpoints[position - 1];
        var upper = breakpoints[position];

        decimal baseFee = _strategy.Calculate(application.Amount, lower, upper);
        return FeeMath.RoundToMultipleOfFive(application.Amount, baseFee);
    }

    private int BinarySearchLeft(List<decimal> array, decimal target)
    {
        int low = 0;
        int high = array.Count;
        while (low < high)
        {
            int mid = low + (high - low) / 2;
            if (array[mid] < target)
                low = mid + 1;
            else
                high = mid;
        }
        return low;
    }
}
