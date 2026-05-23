"""Structured logging and optional error monitoring."""

from __future__ import annotations

import json
import logging
import os
import sys
from datetime import datetime, timezone
from typing import Any


class JsonFormatter(logging.Formatter):
    """Small JSON formatter to keep runtime logs machine-readable."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        for key, value in record.__dict__.items():
            if key.startswith("_") or key in _STANDARD_LOG_RECORD_FIELDS:
                continue
            payload[key] = value

        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)

        return json.dumps(payload, default=str)


def configure_logging(service: str, level: str | None = None) -> logging.Logger:
    """Configure root logging for CLI, dashboard, Docker, and cloud runtimes."""

    log_level = (level or os.getenv("PAGERANKPRO_LOG_LEVEL", "INFO")).upper()
    root = logging.getLogger()
    root.setLevel(log_level)

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(JsonFormatter())
    root.handlers = [handler]

    logger = logging.getLogger(service)
    logger.info("logging_configured", extra={"service": service, "log_level": log_level})
    return logger


def init_error_monitoring(dsn: str | None = None, environment: str | None = None) -> bool:
    """Initialize Sentry when a DSN is provided."""

    sentry_dsn = dsn or os.getenv("SENTRY_DSN")
    if not sentry_dsn:
        return False

    try:
        import sentry_sdk
    except ImportError:
        logging.getLogger(__name__).warning("sentry_sdk_not_installed")
        return False

    sentry_sdk.init(
        dsn=sentry_dsn,
        environment=environment or os.getenv("APP_ENV", "local"),
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0")),
        profiles_sample_rate=float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", "0.0")),
    )
    logging.getLogger(__name__).info("sentry_initialized")
    return True


_STANDARD_LOG_RECORD_FIELDS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
}
