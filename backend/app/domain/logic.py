from decimal import Decimal
from app.domain.constants import FEE_ROUNDING_MULTIPLE, ZERO_DECIMAL

def round_to_multiple_of_five(loan_amount: Decimal, fee: Decimal) -> Decimal:
    total = loan_amount + fee
    remainder = total % FEE_ROUNDING_MULTIPLE
    if remainder == ZERO_DECIMAL:
        return fee
    
    adjustment = FEE_ROUNDING_MULTIPLE - remainder
    return fee + adjustment
