from decimal import Decimal
from typing import List, Tuple
from app.infrastructure.constants import FEE_BREAKPOINTS
from app.domain.interfaces import IFeeRepository

class StaticFeeRepository(IFeeRepository):
    def get_breakpoints(self, term: int) -> List[Tuple[Decimal, Decimal]]:
        raw_data = FEE_BREAKPOINTS.get(term, ())
        breakpoints = [(Decimal(str(x)), Decimal(str(y))) for x, y in raw_data]
        return breakpoints
