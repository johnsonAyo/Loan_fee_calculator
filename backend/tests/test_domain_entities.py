from decimal import Decimal

import pytest

from app.core.exceptions import LoanValidationError
from app.domain.entities import LoanApplication


def test_loan_application_accepts_valid_values():
    application = LoanApplication(amount=Decimal("1000"), term=12)
    assert application.amount == Decimal("1000")
    assert application.term == 12


def test_loan_application_rejects_amount_with_more_than_two_decimals():
    with pytest.raises(LoanValidationError):
        LoanApplication(amount=Decimal("1250.555"), term=12)


def test_loan_application_rejects_non_finite_amount():
    with pytest.raises(LoanValidationError):
        LoanApplication(amount=Decimal("NaN"), term=12)
