"""My audiobook library program."""

__author__ = "Robert Poulin"
__license__ = "MIT"
__version__ = "0.3.1"

from pathlib import Path
import sys


package_folder: str = str(Path(__file__).resolve().parent.parent)
if package_folder not in sys.path:
    sys.path.insert(0, package_folder)
