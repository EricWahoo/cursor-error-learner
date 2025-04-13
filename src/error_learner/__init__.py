"""
Error Learner - A tool for automatic error tracking and learning for Python code.

This package provides functionality to automatically track errors in Python code
and learn from them to suggest improvements and prevent future errors.
"""

__version__ = "1.0.0"
__author__ = "Eric Wahoo"
__email__ = ""

from error_learner.core import track, ErrorTracker
from error_learner.analyzer import PatternAnalyzer
from error_learner.extension import ExtensionTracker

# Create global instances
tracker = ExtensionTracker()
analyzer = PatternAnalyzer()

__all__ = ['track', 'tracker', 'analyzer', 'ErrorTracker', 'PatternAnalyzer'] 