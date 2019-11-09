"""My preconfigured logger."""

__version__ = "2.1.6"
__all__ = ["LogManager"]

import logging
import sys
from copy import copy
from logging import FileHandler, Formatter, Logger, StreamHandler
from pathlib import Path
from time import sleep
from typing import Dict, List, Union

DEFAULT_STREAM_LEVEL: str = "WARNING"
DEFAULT_FILE_LEVEL: str = "DEBUG"


try:
    import colorama

    colorama.init(autoreset=True)
    COLOR: bool = True
except ModuleNotFoundError:
    COLOR = False


class ColoredFormatter(Formatter):
    """Formatter for colored screen output."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if COLOR:
            self.colors: Dict[int, str] = {
                logging.NOTSET: colorama.Fore.WHITE + colorama.Style.DIM,
                logging.DEBUG: colorama.Fore.WHITE + colorama.Style.DIM,
                logging.INFO: colorama.Fore.GREEN + colorama.Style.DIM,
                logging.WARNING: colorama.Fore.BLUE + colorama.Style.BRIGHT,
                logging.ERROR: colorama.Fore.RED + colorama.Style.BRIGHT,
                logging.CRITICAL: colorama.Fore.RED + colorama.Style.BRIGHT,
            }
            self.reset_color: str = colorama.Style.RESET_ALL
        else:
            self.colors = {}
            self.reset_color = ""

    def format(self, record):
        """Format a log record by adding coloring codes."""
        new_record = copy(record)
        color = self.colors.get(new_record.levelno, "")
        new_record.levelname = f"{color}{new_record.levelname:>8}{self.reset_color}"
        new_record.msg = f"{color}{new_record.msg}{self.reset_color}"
        return super().format(new_record)


class LogManager:
    """Logging management class."""

    def __init__(
        self,
        stream_level: Union[str, int, None] = None,
        file_level: Union[str, int, None] = None,
    ) -> None:
        """Initialize a log manager."""
        self._stream_level: str = DEFAULT_STREAM_LEVEL
        self._file_level: str = DEFAULT_FILE_LEVEL
        self.set_default_levels(stream_level, file_level)
        self.loggers: Dict[str, Logger] = {}
        self.file_handlers: Dict[str, FileHandler] = {}
        self.stream_handlers: Dict[str, StreamHandler] = {}
        logging.captureWarnings(capture=True)

    def add_file(
        self,
        logger: Union[Logger, str, None] = None,
        level: Union[str, int, None] = None,
        file: Union[str, Path] = "default.log",
    ) -> FileHandler:
        """Add file handler to logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level, self._file_level)
        log_file: Path = Path(file)
        log_file.touch()
        log_file = log_file.resolve()
        handler: FileHandler = self.file_handlers.get(
            str(log_file), FileHandler(log_file, mode="a", encoding="UTF-8")
        )
        logger.addHandler(handler)
        self.file_handlers.update({str(log_file): handler})
        handler.setLevel(level)
        if log_file.suffix == ".csv":
            handler.setFormatter(
                Formatter(
                    "'%(asctime)s','%(name)s',%(lineno)d,%(levelno)s,'%(message)s'"
                )
            )
        else:
            handler.setFormatter(
                Formatter(
                    "%(asctime)s  %(name)s:%(lineno)03d  %(levelname)-8s  %(message)s"
                )
            )
        return handler

    def add_stream(
        self,
        logger: Union[Logger, str, None] = None,
        level: Union[str, int, None] = None,
    ) -> StreamHandler:
        """Add stream handler to logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level, self._stream_level)
        handlers: List[StreamHandler] = [
            handler for handler in logger.handlers if isinstance(handler, StreamHandler)
        ]
        if handlers:
            handler: StreamHandler = handlers[-1]
        else:
            handler = self.stream_handlers.get(logger.name, StreamHandler(sys.stderr))
        logger.addHandler(handler)
        self.stream_handlers.update({logger.name: handler})
        handler.setLevel(level)
        handler.setFormatter(
            ColoredFormatter(
                fmt=(
                    "%(asctime)s  %(name)s:%(lineno)03d\t%(levelname)s → %(message)s"
                ),
                datefmt="%H:%M:%S",
            )
        )
        return handler

    def close_logger(self, logger: Union[Logger, str, None] = None) -> None:
        """Remove all handlers from the logger and remove it."""
        logger: Logger = self.get_logger(logger)
        self.remove_handlers(logger, files=True, streams=True)
        self.loggers.pop(logger.name, None)

    def flush_logger(self, logger: Union[Logger, str, None] = None) -> None:
        """Flush logger write buffer."""
        sleep(0.2)
        log: Logger = self.get_logger(logger)
        for handler in log.handlers:
            handler.flush()

    def get_level(
        self, level: Union[str, int, None] = None, default: Union[str, int, None] = None
    ) -> int:
        """Get logging level numerical value."""
        level_arg: Union[str, int, None] = level
        if level is None:
            if isinstance(default, int):
                level = default
            else:
                level = self.get_level(default, getattr(logging, self._stream_level))
        if isinstance(level, str):
            level = getattr(logging, level.upper(), None)
        if isinstance(level, int):
            return level
        raise ValueError(f"Unknown logging level: {level_arg}")

    def get_logger(self, logger: Union[Logger, str, None]) -> Logger:
        """Get Logger instance."""
        if isinstance(logger, Logger):
            return logger
        if logger in self.loggers:
            return self.loggers[logger]
        logger = logging.getLogger(logger)
        self.loggers.update({logger.name: logger})
        return logger

    def remove_handlers(
        self,
        logger: Union[Logger, str, None] = None,
        files: bool = False,
        streams: bool = False,
    ) -> None:
        """Remove all handlers of the chosen classes from a logger."""
        logger: Logger = self.get_logger(logger)
        self.flush_logger(logger)
        for handler in logger.handlers:
            handler.close()
            if files and isinstance(handler, FileHandler):
                logger.removeHandler(handler)
                self.file_handlers.pop(handler.baseFilename, None)
            elif streams and isinstance(handler, StreamHandler):
                logger.removeHandler(handler)
                self.stream_handlers.pop(logger.name, None)
        self.set_logger_level(logger)

    def set_default_levels(
        self,
        stream_level: Union[str, int, None] = None,
        file_level: Union[str, int, None] = None,
        setup: bool = False,
    ):
        """Set the default level for new handlers."""
        if stream_level:
            stream_level: int = self.get_level(stream_level)
            self._stream_level = logging.getLevelName(stream_level)
        if file_level:
            file_level: int = self.get_level(file_level)
            self._file_level = logging.getLevelName(file_level)
        if setup:
            for logger in self.loggers:
                self.setup_logger(logger, level=stream_level, stream=True)

    def set_logger_level(self, logger: Union[Logger, str, None] = None) -> None:
        """Set the logger's log level to the minimum required by its handlers."""
        logger: Logger = self.get_logger(logger)
        current_levels: List[int] = [handler.level for handler in logger.handlers]
        new_level: int = min(current_levels) if current_levels else 0
        logger.setLevel(new_level)

    def setup_logger(
        self,
        logger: Union[Logger, str, None] = None,
        level: Union[str, int, None] = None,
        stream: bool = True,
        file: Union[str, Path, None] = None,
    ) -> Logger:
        """Get and configure a logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level)
        if stream:
            self.add_stream(logger=logger, level=level)
        if file:
            self.add_file(logger=logger, file=file)
        self.set_logger_level(logger)
        return logger

    def shutdown(self):
        """Close all loggers and shutdown."""
        for logger in list(self.loggers.values()):
            self.close_logger(logger)
        logging.shutdown()
