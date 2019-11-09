"""Prepares the log manager."""

__author__ = "Robert Poulin"
__license__ = "MIT"
__version__ = "2.0.2-old"
__all__ = ["LogManager"]

from pathlib import Path
import sys


package_folder: str = str(Path(__file__).resolve().parent.parent)
if package_folder not in sys.path:
    sys.path.insert(0, package_folder)


from logs.log_manager import LogManager
