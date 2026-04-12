from pydantic import BaseModel, ConfigDict, Field, field_serializer, field_validator
from decimal import Decimal
from app.core.exceptions import LoanValidationError
from app.domain.constants import LoanTerm, MAX_LOAN_AMOUNT, MIN_LOAN_AMOUNT
from app.domain.entities import LoanApplication
from app.domain.validators import validate_amount_scale as validate_amount_scale_rule

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
        try:
            validate_amount_scale_rule(value)
        except LoanValidationError as error:
            raise ValueError(error.message) from error
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
