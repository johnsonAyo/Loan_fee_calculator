from app import dependencies
from app.infrastructure.repositories.static import StaticFeeRepository
from app.infrastructure.strategies.linear import LinearInterpolationStrategy
from app.services.calculator import FeeCalculatorService


def test_get_fee_repository_returns_static_repository():
    repository = dependencies.get_fee_repository()
    assert isinstance(repository, StaticFeeRepository)


def test_get_interpolation_strategy_returns_linear_strategy():
    strategy = dependencies.get_interpolation_strategy()
    assert isinstance(strategy, LinearInterpolationStrategy)


def test_get_calculator_service_wires_repository_and_strategy():
    repository = dependencies.get_fee_repository()
    strategy = dependencies.get_interpolation_strategy()
    service = dependencies.get_calculator_service(repository, strategy)
    assert isinstance(service, FeeCalculatorService)
    assert service.repository is repository
    assert service.strategy is strategy
