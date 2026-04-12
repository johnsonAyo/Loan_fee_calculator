using System;
using System.Text.Json;
using System.Text.Json.Serialization;
using System.Threading.RateLimiting;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.RateLimiting;
using Microsoft.Extensions.DependencyInjection;
using LoanFeeCalculator.Api.Domain;
using LoanFeeCalculator.Api.Infrastructure;
using LoanFeeCalculator.Api.Services;

// Minimal setup starts here
var builder = WebApplication.CreateBuilder(args);

// Add Dependency Injection
builder.Services.AddScoped<ILoanFeeRepository, StaticFeeRepository>();
builder.Services.AddScoped<IFeeInterpolationStrategy, LinearInterpolationStrategy>();
builder.Services.AddScoped<IFeeCalculatorService, FeeCalculatorService>();

builder.Services.AddCors(options =>
{
    options.AddDefaultPolicy(policy =>
    {
        policy.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod();
    });
});

// Configure Rate Limiter (Fixed Window = 5req/sec)
builder.Services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("ApiPolicy", opt => {
        opt.Window = TimeSpan.FromSeconds(1);
        opt.PermitLimit = 5;
        opt.QueueLimit = 10;
        opt.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
    });
    options.RejectionStatusCode = 429;
});

var app = builder.Build();

app.UseCors();
app.UseRateLimiter();

app.MapGet("/", () => new { status = "online", service = "Loan Fee Calculator", version = "1.0.0" });

app.MapPost("/api/v1/fees/calculate", IResult (LoanRequest request, IFeeCalculatorService service) =>
{
    try
    {
        var application = new LoanApplication(request.Amount, request.Term);
        var fee = service.CalculateFee(application);

        var response = new FeeResponse(
            request.Amount.ToString(),
            request.Term,
            fee.ToString()
        );

        // Emit Structured JSON Telemetry
        var telemetry = new 
        {
            time = DateTime.UtcNow.ToString("O"),
            level = "INFO",
            msg = "calculate_fee_completed",
            @event = "calculate_fee_completed",
            amount = response.Amount,
            term = response.Term,
            fee = response.Fee
        };
        Console.WriteLine(JsonSerializer.Serialize(telemetry));

        return Results.Ok(response);
    }
    catch (LoanValidationError ex)
    {
        return Results.UnprocessableEntity(new ErrorResponse("VALIDATION_ERROR", ex.Message));
    }
    catch (BreakpointNotFoundError ex)
    {
        return Results.UnprocessableEntity(new ErrorResponse("VALIDATION_ERROR", ex.Message));
    }
    catch (CalculationError ex)
    {
        return Results.UnprocessableEntity(new ErrorResponse("VALIDATION_ERROR", ex.Message));
    }
    catch (Exception)
    {
        return Results.Json(new ErrorResponse("INTERNAL_ERROR", "An unexpected error occurred"), statusCode: 500);
    }
}).RequireRateLimiting("ApiPolicy");

app.Run();

// DTOs
public record LoanRequest([property: JsonNumberHandling(JsonNumberHandling.AllowReadingFromString)] decimal Amount, int Term);
public record FeeResponse(string Amount, int Term, string Fee);
public record ErrorResponse(string Code, string Message);
