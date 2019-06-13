"""My preconfigured logger."""

__version__ = "0.0.2"

import logging
import sys
import time
import typing as t
from pathlib import Path


def close_logger(logger: t.Union[logging.Logger, str, None] = None) -> None:
    time.sleep(0.2)
    if isinstance(logger, str):
        logger = logging.getLogger(logger)
    if logger is None or logger.name == "root":
        logging.shutdown()
        return
    for handler in logger.handlers:
        handler.flush()
        handler.close()


def flush_logger(logger: t.Union[logging.Logger, str, None] = None) -> None:
    time.sleep(0.2)
    if not isinstance(logger, logging.Logger):
        logger = logging.getLogger(logger)
    for handler in logger.handlers:
        handler.flush()


def get_logger(
        name: t.Optional[str] = None,
        level: t.Union[str, int] = "WARNING",
        stream: bool = True,
        file: t.Union[str, Path, None] = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    if isinstance(level, str):
        level = getattr(logging, level.upper(), None)
    if level is None:
        raise ValueError(f"Unknown logging level.")
    if file:
        logger.setLevel(logging.DEBUG)
    else:
        if logger.level:
            level = min(level, logger.level)
        logger.setLevel(level)

    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            stream = False
        elif isinstance(handler, logging.FileHandler):
            file = None

    if stream:
        stream_handler = logging.StreamHandler(sys.stderr)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(
            logging.Formatter(
                "%(asctime)s  %(module)s:%(lineno)03d \t%(levelname)-8s ->  %(message)s",
                datefmt="%H:%M:%S",
            )
        )
        logger.addHandler(stream_handler)

    if file:
        file_path: Path = Path(file)
        file_handler = logging.FileHandler(file_path, mode="a", encoding="UTF-8")
        file_handler.setLevel(logging.DEBUG)
        if file_path.suffix == ".csv":
            file_handler.setFormatter(
                logging.Formatter(
                    "'%(asctime)s','%(module)s',%(lineno)d,%(levelno)s,'%(message)s'"
                )
            )
        else:
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s  %(module)s:%(lineno)03d  %(levelname)-8s  %(message)s"
                )
            )
        logger.addHandler(file_handler)

    return logger
