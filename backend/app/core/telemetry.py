import logging
import traceback
from typing import Any
import structlog

LOGGER_NAME = "loan_calculator"

logging.basicConfig(level=logging.INFO, format="%(message)s")
structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso", utc=True, key="timestamp"),
        structlog.stdlib.add_log_level,
        structlog.processors.JSONRenderer(),
    ],
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)
logger = structlog.get_logger(LOGGER_NAME)


def emit_event(level: int, event: str, details: dict[str, Any] | None = None, error: Exception | None = None) -> None:
    payload: dict[str, Any] = {}
    if details:
        payload["details"] = details
    if error is not None:
        payload["error"] = {
            "type": type(error).__name__,
            "message": str(error),
            "stack": "".join(traceback.format_exception(type(error), error, error.__traceback__)),
        }
    if level >= logging.ERROR:
        logger.error(event, **payload)
    elif level >= logging.WARNING:
        logger.warning(event, **payload)
    else:
        logger.info(event, **payload)
