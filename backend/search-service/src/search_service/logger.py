import logging
import sys
from datetime import datetime, timezone


def setup_logger(level: int = logging.DEBUG) -> None:
    colors = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
        "RESET": "\033[0m",
    }

    class ColorFormatter(logging.Formatter):
        def format(self, record: logging.LogRecord) -> str:
            level_color = colors.get(record.levelname, "")
            reset = colors["RESET"]
            record.levelname = f"{level_color}{record.levelname}{reset}"
            record.asctime = datetime.fromtimestamp(record.created, tz=timezone.utc).strftime(
                "%Y-%m-%d %H:%M:%S,%f")[:-3] + " UTC"
            
            message = super().format(record)
            if hasattr(record, 'extra') and record.extra:
                extra_parts = []
                for key, value in record.extra.items():
                    if isinstance(value, (list, dict)):
                        import json
                        extra_parts.append(f"{key}={json.dumps(value)}")
                    else:
                        extra_parts.append(f"{key}={value}")
                if extra_parts:
                    message += " | " + " | ".join(extra_parts)
            
            return message

    formatter = ColorFormatter(fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s")

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)


__all__ = ["setup_logger"]

