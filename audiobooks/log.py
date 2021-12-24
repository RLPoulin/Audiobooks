"""Set up the LogManager."""

import logging
from typing import Literal

from rich.logging import RichHandler

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DEFAULT_LEVEL: LogLevel = "INFO"
MESSAGE_FORMAT: str = "%(message)s"
DATE_FORMAT: str = "%H:%M:%S"


class LogManager:
    """Class to manage loging."""

    def __init__(self, level: LogLevel = DEFAULT_LEVEL):
        """Initialize a log manager.

        Args:
            level: basic logging level, valid values are:
                   "DEBUG", "INFO", "WARNING", "ERROR", and "CRITICAL"
        """
        self.level: LogLevel = level
        logging.basicConfig(
            level=level,
            format=MESSAGE_FORMAT,
            datefmt=DATE_FORMAT,
            handlers=[RichHandler()],
        )
        logging.captureWarnings(capture=True)
        self.loggers: dict[str, logging.Logger] = {}
        self.get_logger(__name__).debug("Logging initialized.")

    def get_logger(self, logger_name: str) -> logging.Logger:
        logger: logging.Logger = self.loggers.get(
            logger_name, logging.getLogger(logger_name)
        )
        self.loggers |= {logger_name: logger}
        return logger

    def set_logger_level(self, logger_name: str, level: LogLevel | None = None) -> None:
        if level is None:
            level = self.level
        self.get_logger(logger_name).setLevel(level)

    def set_all_levels(self, level: LogLevel | None = None) -> None:
        for logger_name in self.loggers:
            self.set_logger_level(logger_name, level)

    def shutdown(self) -> None:
        for logger in self.loggers.values():
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)
        logging.shutdown()


log_manager = LogManager()
