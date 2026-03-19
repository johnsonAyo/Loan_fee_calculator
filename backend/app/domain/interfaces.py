from typing import Protocol, List, Tuple
from decimal import Decimal

class IFeeRepository(Protocol):
    """Interface for fetching fee breakpoints."""
    def get_breakpoints(self, term: int) -> List[Tuple[Decimal, Decimal]]:
        ...

class IFeeInterpolationStrategy(Protocol):
    """Interface for the interpolation logic[cite: 17, 41]."""
    def calculate(self, amount: Decimal, lower_bound: Tuple[Decimal, Decimal], upper_bound: Tuple[Decimal, Decimal]) -> Decimal:
        ...
