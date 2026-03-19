from typing import Any

class FeeCalculationError(Exception):
    error_code = "fee_calculation_error"
    status_code = 400
    expose_details = True

    def __init__(self, message: str, details: dict[str, Any] | None = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}

    def to_response(self) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "error": self.error_code,
            "message": self.message,
        }
        if self.details and self.expose_details:
            payload["details"] = self.details
        return payload


class BusinessRuleError(FeeCalculationError):
    error_code = "business_rule_error"

class ValidationError(FeeCalculationError):
    error_code = "validation_error"

class BreakpointNotFoundError(FeeCalculationError):
    error_code = "breakpoint_not_found"
    expose_details = False

class LoanValidationError(FeeCalculationError):
    error_code = "loan_validation_error"
