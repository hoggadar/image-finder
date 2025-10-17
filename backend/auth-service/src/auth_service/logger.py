import sys
import logging

from datetime import datetime, timezone

def setup_logger(level: int = logging.INFO) -> None:
    COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[41m",
        "RESET": "\033[0m",
    }

    class ColorFormatter(logging.Formatter):
        def format(self, record):
            level_color = COLORS.get(record.levelname, "")
            reset = COLORS["RESET"]
            record.levelname = f"{level_color}{record.levelname}{reset}"
            record.asctime = datetime.fromtimestamp(record.created).strftime("%Y-%m-%d %H:%M:%S")
            return super().format(record)
        
    formatter = ColorFormatter(
        fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.handlers.clear()
    root_logger.addHandler(handler)

    # logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    # logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)