"""
Logging configuration for TalentScout Hiring Assistant
"""
import structlog
import logging
import sys
from pathlib import Path
from typing import Any, Dict

from config.settings import settings

def configure_logging() -> structlog.stdlib.BoundLogger:
    """Configure structured logging"""

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper())
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if settings.DEBUG else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    return structlog.get_logger()

def log_conversation_event(
    logger: structlog.stdlib.BoundLogger,
    event: str,
    session_id: str,
    state: str,
    **kwargs: Any
) -> None:
    """Log conversation events with context"""
    logger.info(
        event,
        session_id=session_id,
        conversation_state=state,
        **kwargs
    )

def log_error(
    logger: structlog.stdlib.BoundLogger,
    error: Exception,
    session_id: str,
    context: Dict[str, Any] = None
) -> None:
    """Log errors with context"""
    logger.error(
        "Error occurred",
        session_id=session_id,
        error_type=type(error).__name__,
        error_message=str(error),
        context=context or {}
    )

# Create global logger instance
logger = configure_logging()
