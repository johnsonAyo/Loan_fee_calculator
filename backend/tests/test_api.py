from decimal import Decimal
from fastapi.testclient import TestClient
from app.core.config import settings
from app.core.exceptions import BreakpointNotFoundError
from app.dependencies import get_calculator_service
from app.main import app


class FailingCalculatorService:
    def calculate_fee(self, application):
        raise BreakpointNotFoundError(
            "Unable to find fee breakpoints for term=12 amount=1500",
            details={"term": 12, "amount": "1500"},
        )


client = TestClient(app)


def test_health_check_returns_service_status():
    response = client.get("/")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "online"
    assert payload["service"] == settings.APP_NAME
    assert payload["version"] == "1.0.0"


def test_calculate_fee_success_case():
    response = client.post("/api/v1/fees/calculate", json={"amount": "2750", "term": 24})
    assert response.status_code == 200
    payload = response.json()
    assert payload["amount"] == "2750"
    assert payload["term"] == 24
    assert payload["fee"] == "115"


def test_calculate_fee_supports_two_decimal_amount():
    response = client.post("/api/v1/fees/calculate", json={"amount": "1250.55", "term": 12})
    assert response.status_code == 200
    payload = response.json()
    total = Decimal(payload["amount"]) + Decimal(payload["fee"])
    assert total % Decimal("5") == Decimal("0")


def test_calculate_fee_rejects_invalid_term():
    response = client.post("/api/v1/fees/calculate", json={"amount": "2750", "term": 36})
    assert response.status_code == 422


def test_calculate_fee_rejects_amount_below_minimum():
    response = client.post("/api/v1/fees/calculate", json={"amount": "999.99", "term": 12})
    assert response.status_code == 422


def test_calculate_fee_rejects_more_than_two_decimal_places():
    response = client.post("/api/v1/fees/calculate", json={"amount": "1250.555", "term": 12})
    assert response.status_code == 422


def test_calculate_fee_accepts_absolute_upper_bound():
    response = client.post("/api/v1/fees/calculate", json={"amount": "20000", "term": 24})
    assert response.status_code == 200
    payload = response.json()
    assert payload["amount"] == "20000"
    assert payload["fee"] == "800"


def test_domain_exception_is_translated_to_api_response():
    app.dependency_overrides[get_calculator_service] = lambda: FailingCalculatorService()
    response = client.post("/api/v1/fees/calculate", json={"amount": "1500", "term": 12})
    app.dependency_overrides.clear()

    assert response.status_code == 400
    payload = response.json()
    assert payload["error"] == "breakpoint_not_found"
    assert "details" not in payload


def test_openapi_contains_request_and_response_examples():
    response = client.get("/openapi.json")
    assert response.status_code == 200
    schema = response.json()
    components = schema["components"]["schemas"]
    request_examples = components["LoanRequest"]["examples"]
    response_examples = components["FeeResponse"]["examples"]
    assert {"amount": "2750", "term": 24} in request_examples
    assert {"amount": "2750", "term": 24, "fee": "115"} in response_examples


def test_calculate_fee_rate_limit_is_enforced():
    statuses = []
    for _ in range(70):
        response = client.post("/api/v1/fees/calculate", json={"amount": "2750", "term": 24})
        statuses.append(response.status_code)
    assert 429 in statuses
