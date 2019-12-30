"""Setup the LogManager."""

__all__ = ["log_manager"]

from myfunctions import LogManager

log_manager = LogManager(stream_level="INFO", file_level="DEBUG")
