from decimal import Decimal
from typing import Literal, TypeAlias

TERM_12 = 12
TERM_24 = 24
LoanTerm: TypeAlias = Literal[12, 24]
VALID_TERMS = (TERM_12, TERM_24)

MIN_LOAN_AMOUNT = Decimal("1000")
MAX_LOAN_AMOUNT = Decimal("20000")
FEE_ROUNDING_MULTIPLE = Decimal("5")
ZERO_DECIMAL = Decimal("0")
