from decimal import Decimal

import pytest

from app.core.exceptions import BreakpointNotFoundError, ValidationError
from app.domain.entities import LoanApplication
from app.infrastructure.repositories.static import StaticFeeRepository
from app.infrastructure.strategies.linear import LinearInterpolationStrategy
from app.services.calculator import FeeCalculatorService


class EmptyFeeRepository:
    def get_breakpoints(self, term: int):
        return []

class UnsortedFeeRepository:
    def get_breakpoints(self, term: int):
        if term == 24:
            return [
                (Decimal("4000"), Decimal("160")),
                (Decimal("2000"), Decimal("100")),
                (Decimal("3000"), Decimal("120")),
            ]
        return []


def test_service_returns_exact_breakpoint_fee():
    service = FeeCalculatorService(StaticFeeRepository(), LinearInterpolationStrategy())
    fee = service.calculate_fee(LoanApplication(amount=Decimal("3000"), term=24))
    assert fee == Decimal("120")


def test_service_interpolates_and_rounds_up():
    service = FeeCalculatorService(StaticFeeRepository(), LinearInterpolationStrategy())
    fee = service.calculate_fee(LoanApplication(amount=Decimal("1100"), term=12))
    assert fee == Decimal("55")


def test_service_handles_fractional_amounts():
    service = FeeCalculatorService(StaticFeeRepository(), LinearInterpolationStrategy())
    fee = service.calculate_fee(LoanApplication(amount=Decimal("1250.55"), term=12))
    assert (fee + Decimal("1250.55")) % Decimal("5") == Decimal("0")


def test_service_handles_absolute_lower_bound():
    service = FeeCalculatorService(StaticFeeRepository(), LinearInterpolationStrategy())
    fee = service.calculate_fee(LoanApplication(amount=Decimal("1000"), term=12))
    assert fee == Decimal("50")


def test_service_handles_absolute_upper_bound():
    service = FeeCalculatorService(StaticFeeRepository(), LinearInterpolationStrategy())
    fee = service.calculate_fee(LoanApplication(amount=Decimal("20000"), term=24))
    assert fee == Decimal("800")


def test_service_raises_breakpoint_not_found_with_details():
    service = FeeCalculatorService(EmptyFeeRepository(), LinearInterpolationStrategy())
    with pytest.raises(BreakpointNotFoundError) as exc_info:
        service.calculate_fee(LoanApplication(amount=Decimal("1500"), term=12))

    exception = exc_info.value
    assert exception.error_code == "breakpoint_not_found"
    assert exception.details["term"] == 12
    assert exception.details["amount"] == "1500"

def test_service_sorts_unsorted_breakpoints_before_lookup():
    service = FeeCalculatorService(UnsortedFeeRepository(), LinearInterpolationStrategy())
    fee = service.calculate_fee(LoanApplication(amount=Decimal("2750"), term=24))
    assert fee == Decimal("115")


def test_linear_strategy_rejects_equal_breakpoint_amounts():
    strategy = LinearInterpolationStrategy()
    with pytest.raises(ValidationError) as exc_info:
        strategy.calculate(
            Decimal("1500"),
            (Decimal("1000"), Decimal("50")),
            (Decimal("1000"), Decimal("90")),
        )

    assert exc_info.value.error_code == "validation_error"
