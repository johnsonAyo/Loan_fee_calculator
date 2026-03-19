from dataclasses import dataclass
from decimal import Decimal
from app.domain.constants import LoanTerm

@dataclass(frozen=True)
class LoanApplication:
    amount: Decimal
    term: LoanTerm
