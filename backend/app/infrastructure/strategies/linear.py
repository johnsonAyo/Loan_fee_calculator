from decimal import Decimal
from app.core.exceptions import ValidationError
from app.domain.interfaces import IFeeInterpolationStrategy

class LinearInterpolationStrategy(IFeeInterpolationStrategy):
    """Values between breakpoints are interpolated linearly[cite: 17]."""
    def calculate(self, amount: Decimal, lower: tuple[Decimal, Decimal], upper: tuple[Decimal, Decimal]) -> Decimal:
        x0, y0 = lower
        x1, y1 = upper
        if x1 == x0:
            raise ValidationError(
                "Invalid breakpoint data for interpolation",
                details={"reason": "equal_breakpoint_amounts"},
            )
        fee = y0 + (amount - x0) * (y1 - y0) / (x1 - x0)
        return fee
