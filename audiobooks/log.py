"""Setup the LogManager."""

__version__ = "0.3.0"
__all__ = ["log_manager"]

from logs import LogManager

log_manager = LogManager(stream_level="INFO", file_level="DEBUG")
