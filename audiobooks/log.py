"""Set up the LogManager."""

import logging

from rich.logging import RichHandler

LEVELS: dict[str, int] = {
    "debug": logging.DEBUG,
    "info": logging.INFO,
    "warning": logging.WARNING,
    "error": logging.ERROR,
}

DEFAULT_LEVEL: str = "info"
MESSAGE_FORMAT: str = "%(message)s"
DATE_FORMAT: str = "%H:%M:%S"


class LogManager:
    def __init__(self, level: str = DEFAULT_LEVEL):
        if level not in LEVELS:
            raise ValueError(f"LogManager: invalid logging level: '{level}'.")
        self.level: str = level
        self._log_level: int = LEVELS[level]
        logging.basicConfig(
            level=self._log_level,
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

    def set_logger_level(self, logger_name: str, level: str | None) -> None:
        logger = self.get_logger(logger_name)
        logger.setLevel(LEVELS.get(level, self._log_level))

    def set_all_levels(self, level: str | None) -> None:
        for logger_name in self.loggers:
            self.set_logger_level(logger_name, level)

    def shutdown(self) -> None:
        for logger in self.loggers.values():
            for handler in logger.handlers:
                handler.close()
                logger.removeHandler(handler)
        logging.shutdown()


log_manager = LogManager()
