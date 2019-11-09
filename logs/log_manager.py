"""My preconfigured logger."""

__version__ = "2.0.2-old"
__all__ = ["LogManager"]

import logging
import sys
from logging import FileHandler, Formatter, Logger, StreamHandler
from pathlib import Path
from time import sleep
from typing import Dict, List, Union

DEFAULT_STREAM_LEVEL: str = "WARNING"
DEFAULT_FILE_LEVEL: str = "DEBUG"


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

    def add_file(
        self,
        logger: Union[Logger, str, None] = None,
        level: Union[str, int, None] = None,
        filename: Union[str, Path] = "default.log",
    ) -> FileHandler:
        """Add file handler to logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level, self._file_level)
        filename: Path = Path(filename)
        filename.touch()
        filename = filename.resolve()
        handler: FileHandler = self.file_handlers.get(
            str(filename), FileHandler(filename, mode="a", encoding="UTF-8")
        )
        logger.addHandler(handler)
        self.file_handlers.update({str(filename): handler})
        handler.setLevel(level)
        if filename.suffix == ".csv":
            handler.setFormatter(
                Formatter(
                    "'%(asctime)s','%(module)s',%(lineno)d,%(levelno)s,'%(message)s'"
                )
            )
        else:
            handler.setFormatter(
                Formatter(
                    "%(asctime)s  %(module)s:%(lineno)03d  %(levelname)-8s  %(message)s"
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
            Formatter(
                "%(asctime)s  %(module)s:%(lineno)03d \t%(levelname)-8s ->  %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        return handler

    def close_logger(self, logger: Union[Logger, str, None] = None) -> None:
        """Close logger or all loggers if root logger."""
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
            if isinstance(handler, FileHandler) and files:
                logger.removeHandler(handler)
                self.file_handlers.pop(handler.baseFilename, None)
            elif isinstance(handler, StreamHandler) and streams:
                logger.removeHandler(handler)
                self.stream_handlers.pop(logger.name, None)

    def set_default_levels(
        self,
        stream_level: Union[str, int, None] = None,
        file_level: Union[str, int, None] = None,
    ):
        """Set the default level for new handlers."""
        if stream_level:
            stream_level: int = self.get_level(stream_level)
            self._stream_level = logging.getLevelName(stream_level)
        if file_level:
            file_level: int = self.get_level(file_level)
            self._file_level = logging.getLevelName(file_level)

    def setup_logger(
        self,
        logger: Union[Logger, str, None] = None,
        level: Union[str, int, None] = None,
        stream: bool = True,
        filename: Union[str, Path, None] = None,
    ) -> Logger:
        """Get and configure a logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level)
        if stream:
            self.add_stream(logger=logger, level=level)
        if filename:
            self.add_file(logger=logger, filename=filename)
        current_levels: List[int] = [level]
        current_levels += [handler.level for handler in logger.handlers]
        logger.setLevel(min(current_levels))
        return logger

    def shutdown(self):
        """Close all loggers and shutdown."""
        for logger in list(self.loggers.values()):
            self.close_logger(logger)
        logging.shutdown()
