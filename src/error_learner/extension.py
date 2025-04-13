"""
Cursor Error Learner Extension - Automatically tracks and learns from errors.
"""

import sys
import logging
import traceback
from datetime import datetime
from typing import Dict, List, Any, Optional
from pathlib import Path

class ErrorTracker:
    """Automatically tracks errors and suggests fixes."""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.error_history = {}
            cls._instance.setup_logging()
            cls._instance.setup_exception_hook()
        return cls._instance
    
    def setup_logging(self):
        """Set up logging configuration."""
        self.logger = logging.getLogger("error_learner")
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
                file_path = tb.tb_frame.f_code.co_filename
                self._track_error(
                    exc_type, 
                    str(exc_value), 
                    func_name, 
                    tb.tb_lineno,
                    file_path
                )
            self.original_hook(exc_type, exc_value, exc_traceback)
        
        sys.excepthook = exception_hook
    
    def _track_error(self, 
                    error_type: type, 
                    error_msg: str, 
                    func_name: str, 
                    line_no: int,
                    file_path: str) -> None:
        """Track an error and provide suggestions if needed."""
        error_key = f"{file_path}:{func_name}"
        if error_key not in self.error_history:
            self.error_history[error_key] = []
        
        self.error_history[error_key].append({
            'timestamp': datetime.now(),
            'type': error_type.__name__,
            'message': str(error_msg),
            'line': line_no,
            'file': file_path
        })
        
        # After 3 occurrences, suggest a fix
        if len(self.error_history[error_key]) >= 3:
            suggestion = self._generate_fix_suggestion(error_type)
            if suggestion:
                self.logger.info(
                    f"Error in {func_name} at {file_path}:{line_no}\n"
                    f"Fix suggestion: {suggestion}"
                )
    
    def _generate_fix_suggestion(self, error_type: type) -> str:
        """Generate fix suggestions based on error type."""
        suggestions = {
            'KeyError': "Ensure the key exists before accessing it: 'if key in dict_name:'",
            'IndexError': "Check if the index is within bounds before accessing",
            'ZeroDivisionError': "Add a check to prevent division by zero: 'if denominator != 0:'",
            'TypeError': "Verify the type of variables before operations",
            'AttributeError': "Check if the object has the attribute before accessing",
            'FileNotFoundError': "Verify file exists before opening: 'if path.exists():'",
            'ValueError': "Validate input values before processing",
        }
        return suggestions.get(error_type.__name__, "Review the error context and add appropriate validation")

# Create global tracker instance
tracker = ErrorTracker()

def get_error_stats() -> Dict[str, List[dict]]:
    """Get all tracked errors."""
    return tracker.error_history.copy()

def get_error_count(file_path: str, function_name: str) -> int:
    """Get error count for a specific function in a file."""
    error_key = f"{file_path}:{function_name}"
    return len(tracker.error_history.get(error_key, [])) 