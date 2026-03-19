# Loan Fee Calculator

## Overview

This project implements a fee calculator for loan applications based on fixed breakpoint tables for 12 and 24 month terms. 

The monorepo solution is split into two workspaces:
- `backend/` FastAPI fee calculation API and Python tests
- `frontend/` Next.js + shadcn/ui application and Playwright tests

The solution includes:
- A domain-oriented backend fee calculation service
- Linear interpolation between fee breakpoints
- Rounding logic that enforces `(loan amount + fee)` to be a multiple of 5
- A FastAPI API endpoint for fee calculation
- A Next.js + shadcn/ui frontend for interactive fee calculation
- A robust automated test suite for domain logic, service behavior, API behavior, and frontend E2E tests

## Requirements Covered

### Backend
- Calculates fee from predefined fee structures for term `12` and `24`
- Supports interpolation for non-breakpoint amounts
- Supports loan amounts with up to 2 decimal places and rejects higher precision values
- Rounds fee upward so total payable is divisible by `5`
- Enforces loan amount bounds of `1000` to `20000`
- Exposes calculation via API: `POST /api/v1/fees/calculate`
- Uses `Decimal` for monetary arithmetic to avoid float precision issues
- Keeps concerns separated by layer (`domain`, `services`, `infrastructure`, `api`, `core`)
- Uses structured custom exceptions with machine-readable error codes and details
- Applies IP-based rate limiting on fee calculation endpoint
- Emits structured JSON telemetry logs for operational observability

### Frontend
- Interactive UI to calculate loan fees based on amount and term
- Validates user input matching backend constraints (amounts up to 2 decimal places, 1000 to 20000 range, term options)
- Displays fee breakdown and exact required repayments
- Seamless client-side integration via `NEXT_PUBLIC_API_BASE_URL`
- Optimized for speed, accessibility, and modern aesthetics using Tailwind CSS and shadcn/ui

## Architecture

### Backend Domain Layer
- `LoanApplication` entity
- Domain constants such as loan bounds and valid terms
- Rounding function `round_to_multiple_of_five`

### Backend Service Layer
- `FeeCalculatorService`:
  - Pulls breakpoints from repository
  - Finds lower/upper bounds
  - Returns exact fee for exact matches
  - Uses interpolation for in-between values
  - Applies rounding rule
  - Raises structured domain exception when bounds are unavailable

### Backend Infrastructure Layer
- `StaticFeeRepository` stores fee breakpoints
- `LinearInterpolationStrategy` encapsulates interpolation math
- Dependency provider registry supports alternative repository and strategy implementations

### Backend API Layer
- `POST /api/v1/fees/calculate`
- Request model validates amount and term
- Request and response schemas include concrete OpenAPI examples
- Response model serializes `Decimal` as string
- Global exception handler maps domain exceptions to API error payloads
- Endpoint rate limiting is applied (`60/minute` per client IP)

### Frontend Layer
- **Next.js App Router**: Utilizes modern Next.js 15 capabilities for fast and SEO-friendly rendering.
- **Components**: shadcn/ui headless components matched with Tailwind CSS for rapid UI development and maintainability.
- **API Integration**: Fetches calculation updates dynamically with built-in error handling and responsive states.

## Error Model

The API error response structure for handled domain errors:

```json
{
  "error": "breakpoint_not_found",
  "message": "Unable to find fee breakpoints for term=12 amount=1500"
}
```

## Test Strategy

The test suite is designed to validate both correctness and integration paths across the entire stack.

### Backend: Domain Tests
- Rounding unchanged when total is already divisible by 5
- Rounding up when total is not divisible by 5
- Linear interpolation computes expected value
- Linear interpolation rejects malformed equal breakpoints
- Property-based checks assert total payable is always divisible by 5 across randomized valid inputs

### Backend: Service Tests
- Exact breakpoint returns expected fee
- Interpolated value is rounded correctly
- Fractional amount still satisfies divisibility rule
- Missing breakpoints raise structured `BreakpointNotFoundError`

### Backend: API Tests
- Health endpoint contract
- Successful fee calculation response
- Two-decimal amount handling
- More-than-two-decimal rejection behavior
- Invalid term validation behavior
- Invalid minimum amount validation behavior
- Domain exception translation into API error payload
- Rate-limit enforcement behavior

### Backend: Dependency Injection Tests
- Alternate repository provider registration and resolution
- Alternate interpolation strategy registration and resolution
- Unsupported provider/strategy validation errors

### Frontend: End-to-End Tests
- Written using **Playwright**
- Covers complete user flows including entering valid/invalid data, submitting the calculation form, and rendering the results
- Ensures visual structure and correct layout rendering across devices

## Pluggable Providers

The backend dependency layer supports selecting and injecting alternative implementations for both data source and interpolation strategy.

Selection by environment:
- `FEE_REPOSITORY_SOURCE` (default: `static`)
- `FEE_INTERPOLATION_STRATEGY` (default: `linear`)

Runtime registration:
- `register_fee_repository_provider(name, factory)`
- `register_interpolation_strategy(name, factory)`

This allows plugging in additional sources such as database-backed or API-backed repositories without changing route or service code.

## How to Run

### Orchestrator Commands (Repository Root)

```bash
make install
make dev
```

`make dev` starts backend on `http://127.0.0.1:8000` and frontend on `http://127.0.0.1:3000`.

Other root commands:
```bash
make dev-backend
make dev-frontend
make test
make lint
make build
make test-e2e
```

### Containerized Run

```bash
docker compose up --build
```

Services:
- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:3000`


### Manual Setup - Backend

```bash
cd backend
python3 -m pip install -r requirements.txt
python3 -m uvicorn app.main:app --reload
```

Static checks and tests:
```bash
python3 -m pytest -q
python3 -m ruff check app
python3 -m mypy app
python3 -m compileall app
```

### Manual Setup - Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend URL: `http://127.0.0.1:3000`
Optional environment variable: `NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000`

## Assumptions

- Loan term is restricted to `12` or `24`
- Loan amount input is expected in GBP-compatible decimal values
- API clients can consume `Decimal` values serialized as strings
- Breakpoint data source is static in this version
- Fee breakpoint amounts are expected to be sorted in ascending order by source
- Because breakpoint ordering is critical to interpolation and binary-search lookup, the service validates ordering at runtime and only sorts when needed
- If breakpoints are already sorted, the service skips sorting to avoid unnecessary overhead

## Architecture Decisions

- ADRs are documented in `docs/adr/`
- 0001 explains the interpolation strategy abstraction
- 0002 explains why decimal fields are serialized as strings in API responses

## Challenges

- Ensuring precision-safe financial calculations across all layers
- Keeping layer boundaries explicit while allowing pragmatic integration
- Managing state updates dynamically within React while maintaining validation sync with the backend
- Handling shared data dependencies elegantly within the serverless environment during deployment

## Trade-offs

- Breakpoints are currently embedded in code for simplicity and determinism; this favors speed of implementation over operational configurability.
- Domain exception status code defaults to `400`; this keeps one consistent client error class.
- Decimal values are returned as strings to preserve precision, which requires clients to parse numeric strings.

## Future Improvements

- Move backend breakpoints to configurable external sources (database, YAML, remote API).
- Introduce versioned API contracts for response evolution.
- Add CI pipeline checks for tests, linting, type checks, and coverage thresholds.
- Expand frontend E2E testing to wider edge cases and visual regression testing.
