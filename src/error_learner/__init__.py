"""
Error Learner - Automatic error tracking and learning for Python code.

This package provides tools for tracking and learning from errors in Python code,
with special integration for the Cursor IDE.
"""

__version__ = "1.0.0"
__author__ = "Eric Wahoo"
__email__ = ""

from .core import ErrorTracker, track
from .analyzer import PatternAnalyzer
from .extension import ExtensionTracker

# Create global instances
tracker = ExtensionTracker()
analyzer = PatternAnalyzer()

__all__ = [
    "track",
    "tracker",
    "analyzer",
    "ErrorTracker",
    "PatternAnalyzer",
    "__version__",
] 