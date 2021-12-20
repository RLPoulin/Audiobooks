"""Set up the LogManager."""

import logging
import time

from rich.logging import RichHandler

STREAM_LEVEL: int = logging.INFO
FORMAT: str = "%(message)s"
DATE_FORMAT: str = "%H:%M:%S"
FLUSH_SLEEP_TIME: float = 0.2


logging.basicConfig(
    level=STREAM_LEVEL, format=FORMAT, datefmt=DATE_FORMAT, handlers=[RichHandler()]
)
logging.captureWarnings(capture=True)
log = logging.getLogger(__name__)
log.debug("logger initialized")


def flush_logger(logger: logging.Logger) -> None:
    """Flush logger write buffer."""
    time.sleep(FLUSH_SLEEP_TIME)
    for log_handler in logger.handlers:
        log_handler.flush()
