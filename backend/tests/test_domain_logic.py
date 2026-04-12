from decimal import Decimal

from app.domain.logic import round_to_multiple_of_five
from app.infrastructure.strategies.linear import LinearInterpolationStrategy


def test_round_to_multiple_of_five_returns_original_when_total_is_multiple():
    fee = round_to_multiple_of_five(Decimal("2000"), Decimal("90"))
    assert fee == Decimal("90")


def test_round_to_multiple_of_five_rounds_up_when_total_is_not_multiple():
    fee = round_to_multiple_of_five(Decimal("1100"), Decimal("54"))
    assert fee == Decimal("55")


def test_linear_interpolation_strategy_calculates_expected_fee():
    strategy = LinearInterpolationStrategy()
    fee = strategy.calculate(
        Decimal("2750"),
        (Decimal("2000"), Decimal("100")),
        (Decimal("3000"), Decimal("120")),
    )
    assert fee == Decimal("115")


def test_linear_interpolation_strategy_handles_flat_fee_bands():
    strategy = LinearInterpolationStrategy()
    fee = strategy.calculate(
        Decimal("1500"),
        (Decimal("1000"), Decimal("50")),
        (Decimal("2000"), Decimal("50")),
    )
    assert fee == Decimal("50")
