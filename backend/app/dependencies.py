from typing import Annotated
from fastapi import Depends
from app.domain.interfaces import IFeeRepository, IFeeInterpolationStrategy
from app.infrastructure.repositories import StaticFeeRepository
from app.infrastructure.strategies import LinearInterpolationStrategy
from app.services import FeeCalculatorService

# 1. Provide the Repository (The Data Source)
def get_fee_repository() -> IFeeRepository:
    """
    Returns the concrete implementation of the fee data source.
    In a real app, you might initialize a DB session here.
    """
    return StaticFeeRepository()

# 2. Provide the Strategy (The Math)
def get_interpolation_strategy() -> IFeeInterpolationStrategy:
    """
    Returns the interpolation logic. Easy to swap if requirements change.
    """
    return LinearInterpolationStrategy()

# 3. Provide the Service (The Orchestrator)
def get_calculator_service(
    repo: Annotated[IFeeRepository, Depends(get_fee_repository)],
    strategy: Annotated[IFeeInterpolationStrategy, Depends(get_interpolation_strategy)]
) -> FeeCalculatorService:
    """
    Injects the repository and strategy into the service.
    This is where the 'Wiring' happens.
    """
    return FeeCalculatorService(repository=repo, strategy=strategy)

# 4. Create a Type Alias for cleaner Route signatures
# This is very similar to NestJS 'Injection Tokens'
CalculatorService = Annotated[FeeCalculatorService, Depends(get_calculator_service)]
