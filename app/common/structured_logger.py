import json
import logging
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """Format application logs as structured JSON."""

    def format(self, record: logging.LogRecord) -> str:
        log_record = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        request_id = getattr(record, "request_id", None)

        if request_id:
            log_record["request_id"] = request_id

        return json.dumps(log_record)


def configure_logging() -> logging.Logger:
    """Configure and return the application logger."""

    logger = logging.getLogger("medical_rag")

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(JsonFormatter())

    logger.addHandler(handler)

    return logger


logger = configure_logging()
