"""
Extension for automatic error tracking in Cursor IDE.
"""

import sys
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional, Type
from pathlib import Path

from .core import ErrorTracker, ErrorInfo

class ExtensionTracker(ErrorTracker):
    """Extended error tracker with Cursor-specific functionality."""
    
    def __init__(self):
        super().__init__()
        self.logger = logging.getLogger("error_learner.extension")
        self.setup_logging()
        self.setup_exception_hook()
        self._error_history: Dict[str, List[Dict[str, Any]]] = {}
    
    def setup_logging(self):
        """Set up logging configuration."""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def setup_exception_hook(self):
        """Set up global exception hook to track all unhandled exceptions."""
        self.original_hook = sys.excepthook
        
        def exception_hook(exc_type, exc_value, exc_traceback):
            """Custom exception hook that tracks errors before handling them."""
            if exc_traceback:
                # Get the actual error location
                tb = exc_traceback
                while tb.tb_next:
                    tb = tb.tb_next
                
                func_name = tb.tb_frame.f_code.co_name
                file_path = Path(tb.tb_frame.f_code.co_filename).resolve()
                self._track_error(
                    exc_type, 
                    str(exc_value), 
                    func_name, 
                    tb.tb_lineno,
                    str(file_path)
                )
            self.original_hook(exc_type, exc_value, exc_traceback)
        
        sys.excepthook = exception_hook
    
    def _track_error(self, 
                    error_type: Type[Exception], 
                    error_msg: str, 
                    func_name: str, 
                    line_no: int,
                    file_path: str) -> None:
        """Track an error and provide suggestions if needed."""
        error_key = f"{file_path}:{func_name}"
        if error_key not in self._error_history:
            self._error_history[error_key] = []
        
        error_entry = {
            'timestamp': datetime.now().isoformat(),
            'error_type': error_type.__name__,
            'message': str(error_msg),
            'line': line_no,
            'file': file_path,
            'count': 1
        }
        
        # Check for similar errors and update count
        for existing in self._error_history[error_key]:
            if (existing['error_type'] == error_entry['error_type'] and 
                existing['line'] == error_entry['line']):
                existing['count'] += 1
                existing['timestamp'] = error_entry['timestamp']
                break
        else:
            self._error_history[error_key].append(error_entry)
        
        # After 3 occurrences, suggest a fix
        total_count = sum(e['count'] for e in self._error_history[error_key] 
                         if e['error_type'] == error_type.__name__)
        if total_count >= 3:
            suggestion = self._generate_fix_suggestion(error_type)
            if suggestion:
                self.logger.info(
                    f"Recurring error in {func_name} at {file_path}:{line_no}\n"
                    f"Fix suggestion: {suggestion}"
                )
    
    def _generate_fix_suggestion(self, error_type: Type[Exception]) -> str:
        """Generate fix suggestions based on error type."""
        suggestions = {
            'KeyError': "Ensure the key exists before accessing it: 'if key in dict_name:'",
            'IndexError': "Check if the index is within bounds before accessing",
            'ZeroDivisionError': "Add a check to prevent division by zero: 'if denominator != 0:'",
            'TypeError': "Verify the type of variables before operations",
            'AttributeError': "Check if the object has the attribute before accessing",
            'FileNotFoundError': "Verify file exists before opening: 'if path.exists():'",
            'ValueError': "Validate input values before processing",
            'ImportError': "Ensure required packages are installed and imported correctly",
            'NameError': "Check variable names and ensure they are defined before use",
            'SyntaxError': "Review code syntax and fix any formatting issues",
        }
        return suggestions.get(error_type.__name__, "Review the error context and add appropriate validation")
    
    @property
    def error_history(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get the error history."""
        return self._error_history.copy()

# Create global instance
tracker = ExtensionTracker()

__all__ = ["ExtensionTracker", "tracker"]

def get_error_stats() -> Dict[str, List[dict]]:
    """Get all tracked errors."""
    return tracker.error_history.copy()

def get_error_count(file_path: str, function_name: str) -> int:
    """Get error count for a specific function in a file."""
    error_key = f"{file_path}:{function_name}"
    return len(tracker.error_history.get(error_key, [])) 