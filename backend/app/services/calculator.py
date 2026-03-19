import logging
from bisect import bisect_left
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
        amounts = [point[LOW_INDEX] for point in breakpoints]
        position = bisect_left(amounts, application.amount)

        if position >= len(breakpoints) or (position == 0 and amounts[position] != application.amount):
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

        if amounts[position] == application.amount:
            rounded_fee = round_to_multiple_of_five(application.amount, breakpoints[position][HIGH_INDEX])
            return rounded_fee

        lower = breakpoints[position - 1]
        upper = breakpoints[position]
        base_fee = self.strategy.calculate(application.amount, lower, upper)
        rounded_fee = round_to_multiple_of_five(application.amount, base_fee)
        return rounded_fee
