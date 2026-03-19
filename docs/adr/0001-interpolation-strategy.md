# ADR 0001: Interpolation Strategy Pattern

## Status
Accepted

## Context
The fee calculator requires interpolation for loan amounts that do not match exact breakpoints. We need interpolation logic that is easy to test and replace without changing service orchestration.

## Decision
Use an interpolation strategy interface in the domain contract and inject a concrete `LinearInterpolationStrategy` from infrastructure.

## Consequences
- Service orchestration remains stable while interpolation math can be replaced.
- Unit testing interpolation behavior is isolated from repository and service concerns.
- Adding future interpolation rules requires only a new strategy implementation and dependency wiring.
