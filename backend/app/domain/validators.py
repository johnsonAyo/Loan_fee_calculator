from decimal import Decimal, InvalidOperation

from app.core.exceptions import LoanValidationError
from app.domain.constants import MAX_LOAN_AMOUNT, MIN_LOAN_AMOUNT, VALID_TERMS


def normalize_amount(raw_amount: Decimal | str | int | float) -> Decimal:
    try:
        normalized_amount = raw_amount if isinstance(raw_amount, Decimal) else Decimal(str(raw_amount))
    except (InvalidOperation, TypeError) as error:
        raise LoanValidationError("Amount must be a valid decimal value") from error
    if not normalized_amount.is_finite():
        raise LoanValidationError(f"Amount {normalized_amount} must be a finite decimal value")
    return normalized_amount


def validate_term(term: int) -> None:
    if term not in VALID_TERMS:
        raise LoanValidationError(f"Invalid term {term}. Must be one of {VALID_TERMS}")


def validate_amount_boundaries_and_precision(amount: Decimal) -> None:
    if amount < MIN_LOAN_AMOUNT or amount > MAX_LOAN_AMOUNT:
        raise LoanValidationError(
            f"Amount {amount} is outside allowed range {MIN_LOAN_AMOUNT}-{MAX_LOAN_AMOUNT}"
        )
    exponent = amount.as_tuple().exponent
    if not isinstance(exponent, int):
        raise LoanValidationError(f"Amount {amount} is not a finite decimal value")
    if exponent < -2:
        raise LoanValidationError(f"Amount {amount} has more than 2 decimal places")
