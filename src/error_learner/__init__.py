"""
Error Learner - Automatic error tracking and learning for Python code.
"""

from .core import track, ErrorTracker
from .analyzer import PatternAnalyzer
from .extension import ErrorTracker as ExtensionTracker

# Create global instances
tracker = ExtensionTracker()
analyzer = PatternAnalyzer()

__all__ = ['track', 'tracker', 'analyzer', 'ErrorTracker', 'PatternAnalyzer'] 