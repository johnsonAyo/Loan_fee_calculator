import logging
from decimal import Decimal
from app.services.constants import (
    BREAKPOINT_NOT_FOUND_ERROR,
    HIGH_INDEX,
    LOW_INDEX,
)
from app.core.exceptions import BreakpointNotFoundError
from app.core.telemetry import emit_event
from app.domain.entities import LoanApplication
from app.domain.interfaces import IFeeRepository, IFeeInterpolationStrategy
from app.domain.logic import round_to_multiple_of_five

class FeeCalculatorService:
    def __init__(
        self,
        repository: IFeeRepository,
        strategy: IFeeInterpolationStrategy,
    ):
        self.repository = repository
        self.strategy = strategy

    def calculate_fee(self, application: LoanApplication) -> Decimal:
        breakpoints = self.repository.get_breakpoints(application.term)
        is_sorted = all(
            breakpoints[index][LOW_INDEX] <= breakpoints[index + 1][LOW_INDEX]
            for index in range(len(breakpoints) - 1)
        )
        if not is_sorted:
            breakpoints = sorted(breakpoints, key=lambda point: point[LOW_INDEX])
        lower = None
        upper = None

        for index in range(len(breakpoints) - 1):
            current = breakpoints[index]
            following = breakpoints[index + 1]
            if current[LOW_INDEX] <= application.amount <= following[LOW_INDEX]:
                lower = current
                upper = following
                break

        if lower is None or upper is None:
            error = BreakpointNotFoundError(
                BREAKPOINT_NOT_FOUND_ERROR.format(term=application.term, amount=application.amount),
                details={
                    "term": application.term,
                    "amount": str(application.amount),
                },
            )
            emit_event(
                logging.ERROR,
                "service_calculate_fee_breakpoint_not_found",
                {"amount": str(application.amount), "term": application.term},
                error,
            )
            raise error

        if lower[LOW_INDEX] == application.amount:
            rounded_fee = round_to_multiple_of_five(application.amount, lower[HIGH_INDEX])
            return rounded_fee
        if upper[LOW_INDEX] == application.amount:
            rounded_fee = round_to_multiple_of_five(application.amount, upper[HIGH_INDEX])
            return rounded_fee

        base_fee = self.strategy.calculate(application.amount, lower, upper)
        rounded_fee = round_to_multiple_of_five(application.amount, base_fee)
        return rounded_fee
