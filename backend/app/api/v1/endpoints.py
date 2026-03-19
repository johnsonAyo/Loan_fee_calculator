import logging
from fastapi import APIRouter, Request
from app.core.rate_limit import CALCULATE_FEE_LIMIT, limiter
from app.dependencies import CalculatorService
from app.schemas.loan import LoanRequest, FeeResponse
from app.core.telemetry import emit_event

router = APIRouter()

@router.post("/calculate", response_model=FeeResponse)
@limiter.limit(CALCULATE_FEE_LIMIT)
async def calculate_fee(
    request: Request,
    payload: LoanRequest,
    service: CalculatorService
):
    try:
        fee = service.calculate_fee(payload.to_domain())
        emit_event(
            logging.INFO,
            "calculate_fee_completed",
            {"amount": str(payload.amount), "term": payload.term, "fee": str(fee)},
        )
        return FeeResponse(amount=payload.amount, term=payload.term, fee=fee)
    except Exception as error:
        emit_event(
            logging.ERROR,
            "calculate_fee_failed",
            {"amount": str(payload.amount), "term": payload.term, "path": str(request.url.path)},
            error,
        )
        raise
