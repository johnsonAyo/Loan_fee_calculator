using System.Collections.Generic;
using LoanFeeCalculator.Api.Domain;

namespace LoanFeeCalculator.Api.Infrastructure;

public class StaticFeeRepository : ILoanFeeRepository
{
    private static readonly Dictionary<int, List<Breakpoint>> _feeBreakpoints = new()
    {
        {
            Constants.Term12, new List<Breakpoint>
            {
                new(1000m, 50m), new(2000m, 90m), new(3000m, 90m), new(4000m, 115m), new(5000m, 100m),
                new(6000m, 120m), new(7000m, 140m), new(8000m, 160m), new(9000m, 180m), new(10000m, 200m),
                new(11000m, 220m), new(12000m, 240m), new(13000m, 260m), new(14000m, 280m), new(15000m, 300m),
                new(16000m, 320m), new(17000m, 340m), new(18000m, 360m), new(19000m, 380m), new(20000m, 400m)
            }
        },
        {
            Constants.Term24, new List<Breakpoint>
            {
                new(1000m, 70m), new(2000m, 100m), new(3000m, 120m), new(4000m, 160m), new(5000m, 200m),
                new(6000m, 240m), new(7000m, 280m), new(8000m, 320m), new(9000m, 360m), new(10000m, 400m),
                new(11000m, 440m), new(12000m, 480m), new(13000m, 520m), new(14000m, 560m), new(15000m, 600m),
                new(16000m, 640m), new(17000m, 680m), new(18000m, 720m), new(19000m, 760m), new(20000m, 800m)
            }
        }
    };

    public List<Breakpoint> GetBreakpoints(int term)
    {
        return _feeBreakpoints.TryGetValue(term, out var breakpoints) ? breakpoints : new List<Breakpoint>();
    }
}
