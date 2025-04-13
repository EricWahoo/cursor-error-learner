"""
Core functionality for error tracking and learning.

This module provides the main decorator and classes for tracking errors
in Python code execution.
"""

import functools
import logging
from typing import Any, Callable, Dict, Optional, Type
from dataclasses import dataclass
from datetime import datetime

@dataclass
class ErrorInfo:
    """Information about a tracked error."""
    timestamp: datetime
    error_type: Type[Exception]
    error_message: str
    function_name: str
    line_number: int
    fix_suggestion: Optional[str] = None

class ErrorTracker:
    """Tracks and analyzes errors in function execution."""
    
    def __init__(self):
        self.error_history: Dict[str, list[ErrorInfo]] = {}
        self.logger = logging.getLogger(__name__)
    
    def track(self, func: Callable) -> Callable:
        """Decorator to track errors in function execution."""
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as e:
                error_info = ErrorInfo(
                    timestamp=datetime.now(),
                    error_type=type(e),
                    error_message=str(e),
                    function_name=func.__name__,
                    line_number=e.__traceback__.tb_lineno
                )
                
                if func.__name__ not in self.error_history:
                    self.error_history[func.__name__] = []
                
                self.error_history[func.__name__].append(error_info)
                self._analyze_error(error_info)
                
                raise
        return wrapper
    
    def _analyze_error(self, error_info: ErrorInfo) -> None:
        """Analyze the error and suggest fixes if possible."""
        func_errors = self.error_history[error_info.function_name]
        if len(func_errors) >= 3:
            # After 3 occurrences, try to suggest a fix
            error_info.fix_suggestion = self._generate_fix_suggestion(error_info)
            self.logger.info(f"Fix suggestion for {error_info.function_name}: {error_info.fix_suggestion}")
    
    def _generate_fix_suggestion(self, error_info: ErrorInfo) -> str:
        """Generate a fix suggestion based on error type and context."""
        if issubclass(error_info.error_type, ZeroDivisionError):
            return "Consider adding a check for zero denominator before division."
        elif issubclass(error_info.error_type, KeyError):
            return "Ensure the key exists in the dictionary before accessing it."
        elif issubclass(error_info.error_type, AttributeError):
            return "Check if the object has the required attribute before accessing it."
        return "Review the error context and implement appropriate error handling."

# Global tracker instance
_tracker = ErrorTracker()

def track(func: Callable) -> Callable:
    """Decorator to track errors in function execution using the global tracker."""
    return _tracker.track(func) 