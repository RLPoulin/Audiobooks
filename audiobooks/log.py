"""Logging functionality."""

import logging
from typing import Literal

from rich.logging import RichHandler

LogLevel = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
DEFAULT_LEVEL: LogLevel = "INFO"
MESSAGE_FORMAT: str = "%(message)s"
DATE_FORMAT: str = "%H:%M:%S"


class LogManager:
    """Class to manage loging."""

    def __init__(self, level: LogLevel):
        """Initialize a log manager.

        Args:
            level: default level ("DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL")
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

    def get_logger(
        self, logger_name: str, level: LogLevel | None = None
    ) -> logging.Logger:
        """Get a specific logger.

        Args:
            logger_name: name of the logger
            level: logging level ("DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL")

        Returns:
            logging.Logger: Logger instance
        """
        if logger_name in self.loggers:
            return self.loggers[logger_name]
        logger: logging.Logger = logging.getLogger(logger_name)
        self.loggers |= {logger_name: logger}
        self.set_logger_level(logger_name, level)
        return logger

    def set_logger_level(self, logger_name: str, level: LogLevel | None = None) -> None:
        """Set the logging level for a logger.

        Args:
            logger_name: name of the logger
            level: logging level ("DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL")
        """
        if level is None:
            level = self.level
        self.get_logger(logger_name).setLevel(level)

    def set_all_levels(
        self, level: LogLevel | None = None, default: bool = False
    ) -> None:
        """Set the logging level for all currently managed loggers.

        Args:
            level: logging level ("DEBUG", "INFO", "WARNING", "ERROR", or "CRITICAL")
            default: if True, change the current default logging level
        """
        if default and level is not None:
            self.level = level
        for logger_name in self.loggers:
            self.set_logger_level(logger_name, level)

    def shutdown(self) -> None:
        """Shutdown the logging system."""
        for logger in self.loggers.values():
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)
        self.loggers = {}
        logging.shutdown()


log_manager = LogManager(DEFAULT_LEVEL)
