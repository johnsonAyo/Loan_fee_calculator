import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi.extension import _rate_limit_exceeded_handler
from app.api.v1.router import api_router
from app.core.config import settings
from app.core.constants import CORS_ORIGINS
from app.core.exceptions import FeeCalculationError
from app.core.rate_limit import limiter
from app.core.telemetry import emit_event

def create_application() -> FastAPI:
    emit_event(logging.INFO, "create_application_started", {"app_name": settings.APP_NAME})
    application = FastAPI(
        title=settings.APP_NAME,
        description="Production-ready Loan Fee Calculation API",
        version="1.0.0",
    )

    application.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.state.limiter = limiter
    application.add_middleware(SlowAPIMiddleware)

    @application.exception_handler(RateLimitExceeded)
    async def rate_limit_exception_handler(request: Request, exc: RateLimitExceeded):
        emit_event(
            logging.WARNING,
            "rate_limit_exceeded",
            {"path": str(request.url.path), "message": str(exc)},
            exc,
        )
        return _rate_limit_exceeded_handler(request, exc)

    @application.exception_handler(FeeCalculationError)
    async def domain_exception_handler(request: Request, exc: FeeCalculationError):
        emit_event(
            logging.ERROR,
            "domain_exception_handler_triggered",
            {"path": str(request.url.path), "status_code": exc.status_code},
            exc,
        )
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.to_response(),
        )

    application.include_router(api_router, prefix="/api/v1")

    @application.get("/", tags=["Health"])
    async def health_check():
        emit_event(logging.INFO, "health_check_called")
        return {
            "status": "online",
            "service": settings.APP_NAME,
            "version": "1.0.0"
        }
    return application

app = create_application()
