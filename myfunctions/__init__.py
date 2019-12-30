"""Robert's module of small tools."""

__authors__ = ["Robert Poulin (poulin.robert@gmail.com)"]
__license__ = "MIT"
__version__ = "2.1.3"
__all__ = ["LogManager"]

from pathlib import Path
import sys


package_folder: str = str(Path(__file__).resolve().parent.parent)
if package_folder not in sys.path:
    sys.path.insert(0, package_folder)


from myfunctions.log_manager import LogManager
