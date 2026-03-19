from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from decimal import Decimal
from app.domain.constants import LoanTerm, MAX_LOAN_AMOUNT, MIN_LOAN_AMOUNT
from app.domain.entities import LoanApplication

class LoanRequest(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"amount": "2750", "term": 24},
                {"amount": "1250.55", "term": 12},
            ]
        }
    )
    amount: Decimal = Field(..., ge=MIN_LOAN_AMOUNT, le=MAX_LOAN_AMOUNT, examples=["2750"])
    term: LoanTerm = Field(..., description="Loan term in months (12 or 24)", examples=[24])

    @field_validator("amount")
    @classmethod
    def validate_amount_scale(cls, value: Decimal) -> Decimal:
        exponent = value.as_tuple().exponent
        if not isinstance(exponent, int):
            raise ValueError("Amount must be a finite decimal value")
        if exponent < -2:
            raise ValueError("Amount must have at most 2 decimal places")
        return value

    def to_domain(self) -> LoanApplication:
        return LoanApplication(amount=self.amount, term=self.term)

class FeeResponse(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {"amount": "2750", "term": 24, "fee": "115"},
            ]
        }
    )
    amount: Decimal
    term: LoanTerm
    fee: Decimal

    @field_serializer("amount", "fee")
    def serialize_decimal(self, value: Decimal) -> str:
        return str(value)
