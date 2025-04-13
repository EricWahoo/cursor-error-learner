"""
Error Learner - A tool for tracking and learning from Python errors.

This package provides functionality to track, analyze, and learn from errors
in Python code execution.
"""

__version__ = "1.0.0"

from .core import track, ErrorTracker, ErrorInfo
from .utils import setup_logging, get_error_stats, get_error_count

__all__ = [
    'track',
    'ErrorTracker',
    'ErrorInfo',
    'setup_logging',
    'get_error_stats',
    'get_error_count'
] 