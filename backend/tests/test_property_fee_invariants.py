from decimal import Decimal

from hypothesis import given, settings
from hypothesis import strategies as st

from app.domain.constants import LoanTerm
from app.domain.entities import LoanApplication
from app.infrastructure.repositories.static import StaticFeeRepository
from app.infrastructure.strategies.linear import LinearInterpolationStrategy
from app.services.calculator import FeeCalculatorService


@settings(max_examples=1000)
@given(
    amount=st.decimals(
        min_value=Decimal("1000"),
        max_value=Decimal("20000"),
        places=2,
        allow_nan=False,
        allow_infinity=False,
    ),
    term=st.sampled_from([12, 24]),
)
def test_total_payable_is_always_multiple_of_five(amount: Decimal, term: LoanTerm):
    service = FeeCalculatorService(StaticFeeRepository(), LinearInterpolationStrategy())
    fee = service.calculate_fee(LoanApplication(amount=amount, term=term))
    assert (amount + fee) % Decimal("5") == Decimal("0")
