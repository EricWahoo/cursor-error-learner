"""
Utility functions for error tracking and analysis.
"""

import logging
from typing import Dict, List, Optional, Union

def setup_logging(name: str) -> logging.Logger:
    """
    Set up logging configuration.
    
    Args:
        name: Name for the logger
        
    Returns:
        Configured logger instance
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(levelname)s  %(name)s:%(filename)s:%(lineno)d %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(logging.INFO)
    return logger

def get_error_stats(error_history: Dict[str, List[Dict]]) -> Dict[str, Union[int, Dict[str, int]]]:
    """
    Get statistics about tracked errors.
    
    Args:
        error_history: Dictionary mapping function names to lists of error info
        
    Returns:
        Dictionary with error statistics
    """
    stats = {"total_errors": 0, "error_types": {}}
    for errors in error_history.values():
        for error in errors:
            error_type = error["error_type"]
            count = error.get("count", 1)
            stats["total_errors"] += count
            stats["error_types"][error_type] = stats["error_types"].get(error_type, 0) + count
    return stats

def get_error_count(error_history: Dict[str, List[Dict]], function_name: str) -> int:
    """
    Get the number of errors tracked for a specific function.
    
    Args:
        error_history: Dictionary mapping function names to lists of error info
        function_name: Name of the function to check
        
    Returns:
        Number of errors tracked for the function
    """
    errors = error_history.get(function_name, [])
    return sum(error.get("count", 1) for error in errors) 