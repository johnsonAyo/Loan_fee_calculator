from dataclasses import dataclass
from decimal import Decimal
from app.domain.constants import LoanTerm
from app.domain.validators import (
    normalize_amount,
    validate_amount_boundaries_and_precision,
    validate_term,
)


@dataclass(frozen=True)
class LoanApplication:
    amount: Decimal
    term: LoanTerm

    def __post_init__(self):
        normalized_amount = normalize_amount(self.amount)
        object.__setattr__(self, "amount", normalized_amount)
        validate_term(self.term)
        validate_amount_boundaries_and_precision(self.amount)
