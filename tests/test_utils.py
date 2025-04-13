"""
Tests for the utility functions.
"""

import logging
from error_learner.utils import setup_logging, get_error_stats, get_error_count

def test_setup_logging():
    """Test logging setup."""
    logger = setup_logging("test")
    assert isinstance(logger, logging.Logger)
    assert logger.name == "test"

def test_get_error_stats():
    """Test getting error statistics."""
    error_history = {
        "func1": [
            {"error_type": "ZeroDivisionError", "count": 2},
            {"error_type": "KeyError", "count": 1}
        ],
        "func2": [
            {"error_type": "TypeError", "count": 1}
        ]
    }
    
    stats = get_error_stats(error_history)
    assert stats["total_errors"] == 4
    assert stats["error_types"]["ZeroDivisionError"] == 2
    assert stats["error_types"]["KeyError"] == 1
    assert stats["error_types"]["TypeError"] == 1

def test_get_error_count():
    """Test getting error count."""
    error_history = {
        "func1": [
            {"error_type": "ZeroDivisionError", "count": 2},
            {"error_type": "KeyError", "count": 1}
        ]
    }
    
    count = get_error_count(error_history, "func1")
    assert count == 3
    
    count = get_error_count(error_history, "nonexistent")
    assert count == 0 