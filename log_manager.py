"""My preconfigured logger."""
__version__ = "2.0.0"

import logging
from logging import FileHandler, Formatter, Logger, StreamHandler
from pathlib import Path
import sys
from time import sleep
import typing as t


class LogManager:
    """Logging management class."""

    stream_level = "WARNING"
    file_level = "DEBUG"

    def __init__(
            self,
            stream_level: t.Union[str, int] = stream_level,
            file_level: t.Union[str, int] = file_level,
    ) -> None:
        self.set_default_levels(stream_level, file_level)
        self.loggers: t.Dict[str, Logger] = {}
        self.file_handlers: t.Dict[str, FileHandler] = {}
        self.stream_handlers: t.Dict[str, StreamHandler] = {}

    def add_file(
            self,
            logger: t.Union[Logger, str, None] = None,
            level: t.Union[str, int, None] = None,
            file: t.Union[str, Path] = "default.log",
    ) -> FileHandler:
        """Add file handler to logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level, self.file_level)
        file: Path = Path(file)
        file.touch()
        file = file.resolve()
        handler: FileHandler = self.file_handlers.get(
            str(file), FileHandler(file, mode="a", encoding="UTF-8")
        )
        logger.addHandler(handler)
        self.file_handlers.update({str(file): handler})
        handler.setLevel(level)
        if file.suffix == ".csv":
            handler.setFormatter(
                Formatter("'%(asctime)s','%(module)s',%(lineno)d,%(levelno)s,'%(message)s'")
            )
        else:
            handler.setFormatter(
                Formatter("%(asctime)s  %(module)s:%(lineno)03d  %(levelname)-8s  %(message)s")
            )
        return handler

    def add_stream(
            self, logger: t.Union[Logger, str, None] = None, level: t.Union[str, int, None] = None
    ) -> StreamHandler:
        """Add stream handler to logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level, self.stream_level)
        handlers: t.List[StreamHandler] = [
            h for h in logger.handlers if isinstance(h, StreamHandler)
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

    def close_logger(self, logger: t.Union[Logger, str, None] = None) -> None:
        """Close logger or all loggers if root logger."""
        logger: Logger = self.get_logger(logger)
        self.remove_handlers(logger, files=True, streams=True)
        if logger.name in self.loggers.keys():
            del self.loggers[logger.name]

    def flush_logger(self, logger: t.Union[Logger, str, None] = None) -> None:
        """Flush logger write buffer."""
        sleep(0.2)
        log: Logger = self.get_logger(logger)
        for handler in log.handlers:
            handler.flush()

    def get_level(
            self, level: t.Union[str, int, None] = None, default: t.Union[str, int, None] = None
    ) -> int:
        """Get logging level numerical value."""
        if level is None:
            if isinstance(default, int):
                level: int = default
            else:
                level = self.get_level(default, getattr(logging, self.stream_level))
        if isinstance(level, int):
            return level
        value: int = getattr(logging, level.upper(), None)
        if isinstance(value, int):
            return value
        else:
            raise ValueError(f"Unknown logging level: {level}")

    def get_logger(self, logger: t.Union[Logger, str, None]) -> Logger:
        """Get Logger instance."""
        if isinstance(logger, Logger):
            return logger
        if logger in self.loggers:
            return self.loggers[logger]
        logger = logging.getLogger(logger)
        self.loggers.update({logger.name: logger})
        return logger

    def remove_handlers(
            self, logger: t.Union[Logger, str, None] = None, files: bool = False,
            streams: bool = False
    ) -> None:
        """Remove all handlers of the chosen classes from a logger."""
        logger: Logger = self.get_logger(logger)
        self.flush_logger(logger)
        for handler in logger.handlers:
            handler.close()
            if isinstance(handler, FileHandler) and files:
                logger.removeHandler(handler)
                if handler.baseFilename in self.file_handlers:
                    del self.file_handlers[handler.baseFilename]
            elif isinstance(handler, StreamHandler) and streams:
                logger.removeHandler(handler)
                if logger.name in self.stream_handlers:
                    del self.stream_handlers[logger.name]

    def set_default_levels(
            self,
            stream_level: t.Union[str, int, None] = None,
            file_level: t.Union[str, int, None] = None,
    ):
        if stream_level:
            stream_level: int = self.get_level(stream_level)
            self.stream_level = logging.getLevelName(stream_level)
        if file_level:
            file_level: int = self.get_level(file_level)
            self.file_level = logging.getLevelName(file_level)

    def setup_logger(
            self,
            logger: t.Union[Logger, str, None] = None,
            level: t.Union[str, int, None] = None,
            stream: bool = True,
            file: t.Union[str, Path, None] = None,
    ) -> Logger:
        """Get and configure a logger."""
        logger: Logger = self.get_logger(logger)
        level: int = self.get_level(level)
        if stream:
            self.add_stream(logger=logger, level=level)
        if file:
            self.add_file(logger=logger, file=file)
        logger.setLevel(min([level] + [h.level for h in logger.handlers]))
        return logger

    def shutdown(self):
        """Close all loggers and shutdown."""
        for logger in list(self.loggers.values()):
            self.close_logger(logger)
        logging.shutdown()
