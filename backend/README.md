# Loan Fee Calculation

## Overview

This project implements a backend fee calculator for loan applications based on fixed breakpoint tables for 12 and 24 month terms.

The solution includes:

- A domain-oriented fee calculation service
- Linear interpolation between fee breakpoints
- Rounding logic that enforces `(loan amount + fee)` to be a multiple of 5
- A FastAPI API endpoint for fee calculation
- A Next.js + shadcn/ui frontend for interactive fee calculation
- A robust automated test suite for domain logic, service behavior, and API behavior

## Requirements Covered

### Functional

- Calculates fee from predefined fee structures for term `12` and `24`
- Supports interpolation for non-breakpoint amounts
- Supports loan amounts with up to 2 decimal places and rejects higher precision values
- Rounds fee upward so total payable is divisible by `5`
- Enforces loan amount bounds of `1000` to `20000`
- Exposes calculation via API: `POST /api/v1/fees/calculate`

### Engineering

- Uses `Decimal` for monetary arithmetic to avoid float precision issues
- Enforces amount precision to maximum 2 decimal places
- Keeps concerns separated by layer:
  - `domain` for business primitives and rules
  - `services` for orchestration
  - `infrastructure` for data source and strategy implementations
  - `api` for transport layer concerns
  - `core` for runtime/app concerns
- Uses structured custom exceptions with machine-readable error codes and details
- Applies IP-based rate limiting on fee calculation endpoint
- Emits structured JSON telemetry logs for operational observability

## Architecture

### Domain Layer

- `LoanApplication` entity
- Domain constants such as loan bounds and valid terms
- Rounding function `round_to_multiple_of_five`

### Service Layer

- `FeeCalculatorService`:
  - Pulls breakpoints from repository
  - Finds lower/upper bounds
  - Returns exact fee for exact matches
  - Uses interpolation for in-between values
  - Applies rounding rule
  - Raises structured domain exception when bounds are unavailable

### Infrastructure Layer

- `StaticFeeRepository` stores fee breakpoints
- `LinearInterpolationStrategy` encapsulates interpolation math
- Dependency provider registry supports alternative repository and strategy implementations

### API Layer

- `POST /api/v1/fees/calculate`
- Request model validates amount and term
- Request and response schemas include concrete OpenAPI examples
- Response model serializes `Decimal` as string
- Global exception handler maps domain exceptions to API error payloads
- Endpoint rate limiting is applied (`60/minute` per client IP)

### Frontend Layer

- Next.js App Router application in `frontend/`
- shadcn/ui components for form, feedback, and result rendering
- Client-side integration with backend API using `NEXT_PUBLIC_API_BASE_URL`

## Error Model

The API error response structure for handled domain errors:

```json
{
  "error": "breakpoint_not_found",
  "message": "Unable to find fee breakpoints for term=12 amount=1500"
}
```

## Test Strategy

The suite is designed to validate both correctness and integration paths.

### Domain Tests

- Rounding unchanged when total is already divisible by 5
- Rounding up when total is not divisible by 5
- Linear interpolation computes expected value
- Linear interpolation rejects malformed equal breakpoints

### Service Tests

- Exact breakpoint returns expected fee
- Interpolated value is rounded correctly
- Fractional amount still satisfies divisibility rule
- Missing breakpoints raise structured `BreakpointNotFoundError`

### API Tests

- Health endpoint contract
- Successful fee calculation response
- Two-decimal amount handling
- More-than-two-decimal rejection behavior
- Invalid term validation behavior
- Invalid minimum amount validation behavior
- Domain exception translation into API error payload
- OpenAPI schema examples presence
- Rate-limit enforcement behavior

### Dependency Injection Tests

- Alternate repository provider registration and resolution
- Alternate interpolation strategy registration and resolution
- Unsupported provider/strategy validation errors

## Pluggable Providers

The dependency layer supports selecting and injecting alternative implementations for both data source and interpolation strategy.

Selection by environment:

- `FEE_REPOSITORY_SOURCE` (default: `static`)
- `FEE_INTERPOLATION_STRATEGY` (default: `linear`)

Runtime registration:

- `register_fee_repository_provider(name, factory)`
- `register_interpolation_strategy(name, factory)`

This allows plugging in additional sources such as database-backed or API-backed repositories without changing route or service code.

## How to Run

### Install dependencies

```bash
python3 -m pip install -r requirements.txt
```

### Run API

```bash
python3 -m uvicorn app.main:app --reload
```

### Run frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL:

```bash
http://127.0.0.1:3000
```

Optional frontend environment variable:

```bash
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
```

### Run tests

```bash
python3 -m pytest -q
```

### Static checks

```bash
python3 -m ruff check app
python3 -m mypy app
python3 -m compileall app
```

## Assumptions

- Loan term is restricted to `12` or `24`
- Loan amount input is expected in GBP-compatible decimal values
- API clients can consume `Decimal` values serialized as strings
- Breakpoint data source is static in this version

## Challenges

- Ensuring precision-safe financial calculations across all layers
- Preserving readability while balancing constants reuse vs inline route clarity
- Keeping layer boundaries explicit while allowing pragmatic integration
- Making exception payloads useful for API clients and debugging

## Trade-offs

- Breakpoints are currently embedded in code for simplicity and determinism; this favors speed of implementation over operational configurability
- Domain exception status code defaults to `400`; this keeps one consistent client error class, though some teams may prefer `404` for missing breakpoint data
- Decimal values are returned as strings to preserve precision, which requires clients to parse numeric strings

## Future Improvements

- Move breakpoints to configurable external sources (database, YAML, remote API)
- Introduce versioned API contracts for response evolution
- Add CI pipeline checks for tests, linting, type checks, and coverage thresholds
