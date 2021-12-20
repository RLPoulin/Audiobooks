"""Set up the LogManager."""

import logging

from rich.logging import RichHandler

DEFAULT_LEVEL: int = logging.INFO
FORMAT: str = "%(message)s"
DATE_FORMAT: str = "%H:%M:%S"


logging.basicConfig(
    level=DEFAULT_LEVEL, format=FORMAT, datefmt=DATE_FORMAT, handlers=[RichHandler()]
)
logging.captureWarnings(capture=True)


class LogManager:
    LEVELS: dict[str, int] = {
        "debug": logging.DEBUG,
        "info": logging.INFO,
        "warning": logging.WARNING,
        "error": logging.ERROR,
    }

    def __init__(self):
        self.loggers: dict[str, logging.Logger] = {}

    def get_logger(self, logger_name: str) -> logging.Logger:
        logger: logging.Logger = self.loggers.get(
            logger_name, logging.getLogger(logger_name)
        )
        self.loggers |= {logger_name: logger}
        return logger

    def set_logger_level(self, logger_name: str, level: str) -> None:
        logger = self.get_logger(logger_name)
        logger.setLevel(self.LEVELS.get(level, DEFAULT_LEVEL))

    def shutdown(self) -> None:
        for logger in self.loggers.values():
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)
        logging.shutdown()


log_manager = LogManager()
log = log_manager.get_logger(__name__)
log.debug("Logging initialized")
