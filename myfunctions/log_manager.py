"""My preconfigured logger.

TODO: docstrings

"""

__all__ = ["LogManager"]

from copy import copy
import logging
from pathlib import Path
import sys
import time
from typing import Dict, List, Optional, Union

try:
    import colorama

    colorama.init(autoreset=True)
    COLOR: bool = True
except ModuleNotFoundError:
    COLOR = False

Level = Union[int, str]
Log = Union[logging.Logger, str]
PathLike = Union[Path, str]

DEFAULT_STREAM_LEVEL: str = "WARNING"
DEFAULT_FILE_LEVEL: str = "DEBUG"
STREAM_FORMAT: str = "%(asctime)s  %(name)s:%(lineno)03d\t%(levelname)s → %(message)s"
FILE_FORMAT: str = "%(asctime)s  %(name)s:%(lineno)03d  %(levelname)-8s  %(message)s"
CSV_FORMAT: str = "'%(asctime)s','%(name)s',%(lineno)d,%(levelno)s,'%(message)s'"


class ColoredFormatter(logging.Formatter):
    """Formatter for colored screen output."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if COLOR:
            self.colors: Dict[int, str] = {
                logging.NOTSET: colorama.Fore.WHITE + colorama.Style.DIM,
                logging.DEBUG: colorama.Fore.WHITE + colorama.Style.DIM,
                logging.INFO: colorama.Fore.GREEN + colorama.Style.DIM,
                logging.WARNING: colorama.Fore.YELLOW + colorama.Style.BRIGHT,
                logging.ERROR: colorama.Fore.RED + colorama.Style.BRIGHT,
                logging.CRITICAL: colorama.Fore.MAGENTA + colorama.Style.BRIGHT,
            }
            self.reset_color: str = colorama.Style.RESET_ALL
        else:
            self.colors = {}
            self.reset_color = ""

    def format(self, record: logging.LogRecord):
        """Format a log record by adding coloring codes."""
        new_record: logging.LogRecord = copy(record)
        color: str = self.colors.get(new_record.levelno, "")
        new_record.levelname = f"{color}{new_record.levelname:>8}{self.reset_color}"
        new_record.msg = f"{color}{new_record.msg}{self.reset_color}"
        return super().format(new_record)


class LogManager:
    """Logging management class."""

    def __init__(
        self, stream_level: Optional[Level] = None, file_level: Optional[Level] = None
    ) -> None:
        """Initialize a log manager."""
        self._stream_level: str = DEFAULT_STREAM_LEVEL
        self._file_level: str = DEFAULT_FILE_LEVEL
        self.set_default_levels(stream_level, file_level, setup_loggers=False)
        self.loggers: Dict[str, logging.Logger] = {}
        self.file_handlers: Dict[str, logging.FileHandler] = {}
        self.stream_handlers: Dict[str, logging.StreamHandler] = {}
        logging.captureWarnings(capture=True)

    def set_default_levels(
        self,
        stream_level: Optional[Level] = None,
        file_level: Optional[Level] = None,
        *,
        setup_loggers: bool = False,
    ) -> None:
        """Set the default level for new handlers."""
        if stream_level is not None:
            stream_level: int = self.get_level(stream_level)
            self._stream_level = logging.getLevelName(stream_level)
        if file_level is not None:
            file_level: int = self.get_level(file_level)
            self._file_level = logging.getLevelName(file_level)
        if not setup_loggers:
            return
        for logger in self.loggers:
            self.setup_logger(logger, stream_level=stream_level, file_level=file_level)

    def setup_logger(
        self,
        logger: Optional[Log] = None,
        *,
        add_stream: bool = True,
        stream_level: Optional[Level] = None,
        add_file: bool = False,
        file: Optional[PathLike] = None,
        file_level: Optional[Level] = None,
    ) -> logging.Logger:
        """Get and configure a logger."""
        logger: logging.Logger = self.get_logger(logger)
        if add_stream:
            self.add_stream(logger=logger, level=stream_level)
        if add_file:
            self.add_file(logger=logger, level=file_level, log_file=file)
        for handler in logger.handlers:
            if stream_level is not None and isinstance(handler, logging.StreamHandler):
                handler.setLevel(stream_level)
            if file_level is not None and isinstance(handler, logging.FileHandler):
                handler.setLevel(file_level)
        self._set_logger_level(logger)
        return logger

    def get_logger(self, logger: Optional[Log]) -> logging.Logger:
        """Get Logger instance."""
        if isinstance(logger, logging.Logger):
            return logger
        if logger in self.loggers:
            return self.loggers[logger]
        logger: logging.Logger = logging.getLogger(logger)
        self.loggers.update({logger.name: logger})
        return logger

    def get_level(
        self, level: Optional[Level] = None, default: Optional[Level] = None
    ) -> int:
        """Get logging level numerical value."""
        level_arg: Optional[Level] = level
        if level is None:
            if isinstance(default, int):
                return default
            level = self.get_level(default, getattr(logging, self._stream_level))
        if isinstance(level, str):
            level = getattr(logging, level.upper(), None)
        if isinstance(level, int):
            return level
        raise ValueError(f"Unknown logging level: {level_arg}")

    def add_stream(
        self, logger: Optional[Log] = None, level: Optional[Level] = None
    ) -> logging.StreamHandler:
        """Add stream handler to logger."""
        logger: logging.Logger = self.get_logger(logger)
        level: int = self.get_level(level, self._stream_level)

        handlers: List[logging.StreamHandler] = [
            handler
            for handler in logger.handlers
            if isinstance(handler, logging.StreamHandler)
        ]
        if handlers:
            handler: logging.StreamHandler = handlers[-1]
        else:
            handler = self.stream_handlers.get(
                logger.name, logging.StreamHandler(sys.stderr)
            )

        logger.addHandler(handler)
        self.stream_handlers.update({logger.name: handler})
        handler.setLevel(level)
        handler.setFormatter(ColoredFormatter(fmt=STREAM_FORMAT, datefmt="%H:%M:%S"))

        return handler

    def add_file(
        self,
        logger: Optional[Log] = None,
        log_file: Optional[PathLike] = None,
        level: Optional[Level] = None,
    ) -> logging.FileHandler:
        """Add file handler to logger."""
        logger: logging.Logger = self.get_logger(logger)
        level: int = self.get_level(level, self._file_level)
        log_file: PathLike = log_file if log_file else f"{logger.name}.log"
        log_file: Path = Path(log_file)

        log_file.touch()
        log_file = log_file.resolve()
        handler: logging.FileHandler = self.file_handlers.get(
            str(log_file), logging.FileHandler(log_file, mode="a", encoding="UTF-8")
        )

        logger.addHandler(handler)
        self.file_handlers.update({str(log_file): handler})
        handler.setLevel(level)
        log_format: str = CSV_FORMAT if log_file.suffix == ".csv" else FILE_FORMAT
        handler.setFormatter(logging.Formatter(log_format))

        return handler

    def flush_logger(self, logger: Optional[Log] = None) -> None:
        """Flush logger write buffer."""
        time.sleep(0.2)
        logger: logging.Logger = self.get_logger(logger)
        for handler in logger.handlers:
            handler.flush()

    def remove_handlers(
        self,
        logger: Optional[Log] = None,
        *,
        files: bool = False,
        streams: bool = False,
    ) -> None:
        """Remove all handlers of the chosen classes from a logger."""
        logger: logging.Logger = self.get_logger(logger)
        self.flush_logger(logger)
        for handler in logger.handlers:
            if streams and isinstance(handler, logging.StreamHandler):
                self.stream_handlers.pop(logger.name, None)
            elif files and isinstance(handler, logging.FileHandler):
                self.file_handlers.pop(handler.baseFilename, None)
            else:
                continue
            handler.close()
            logger.removeHandler(handler)
        self._set_logger_level(logger)

    def close_logger(self, logger: Optional[Log] = None) -> None:
        """Close logger or all loggers if root logger."""
        logger: logging.Logger = self.get_logger(logger)
        self.remove_handlers(logger, files=True, streams=True)
        self.loggers.pop(logger.name, None)

    def shutdown(self):
        """Close all loggers and shutdown."""
        for logger in list(self.loggers.values()):
            self.close_logger(logger)
        logging.shutdown()

    def _set_logger_level(self, logger: Optional[Log] = None) -> None:
        """Set the logger's log level to the minimum required by its handlers."""
        logger: logging.Logger = self.get_logger(logger)
        current_levels: List[int] = [handler.level for handler in logger.handlers]
        new_level: int = min(current_levels) if current_levels else 0
        logger.setLevel(new_level)
