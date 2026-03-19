# ADR 0002: Serialize Decimal Values as Strings in API Responses

## Status
Accepted

## Context
The backend uses `Decimal` for financial precision. JSON numeric values can lose precision or be parsed differently across clients.

## Decision
Serialize `Decimal` fields (`amount`, `fee`) as strings in API responses.

## Consequences
- Precision is preserved across language runtimes and clients.
- Clients must parse numeric strings when they need arithmetic.
- API behavior is explicit and predictable for financial payloads.
