"""
Utility functions for error tracking and logging.

This module provides helper functions for setting up logging and
retrieving error statistics.
"""

import logging
from typing import Dict, List
from datetime import datetime
from .core import ErrorTracker, ErrorInfo

def setup_logging(level: int = logging.INFO) -> None:
    """
    Set up logging configuration for the error tracker.
    
    Args:
        level: The logging level to use (default: logging.INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

def get_error_stats(tracker: ErrorTracker) -> Dict[str, List[ErrorInfo]]:
    """
    Get statistics about tracked errors.
    
    Args:
        tracker: The ErrorTracker instance to analyze
        
    Returns:
        Dictionary mapping function names to lists of ErrorInfo objects
    """
    return tracker.error_history.copy()

def get_error_count(tracker: ErrorTracker, function_name: str) -> int:
    """
    Get the number of errors tracked for a specific function.
    
    Args:
        tracker: The ErrorTracker instance to analyze
        function_name: Name of the function to check
        
    Returns:
        Number of errors tracked for the function
    """
    return len(tracker.error_history.get(function_name, [])) 