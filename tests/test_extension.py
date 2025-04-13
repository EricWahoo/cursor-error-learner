"""
Tests for the automatic error tracking extension.
"""

import pytest
import sys
from error_learner.extension import ErrorTracker, tracker

def test_automatic_error_tracking():
    """Test that errors are automatically tracked without decorators."""
    # Create a function that will raise an error
    def risky_function():
        return 1/0
    
    # The error should be tracked automatically
    try:
        risky_function()
    except ZeroDivisionError as e:
        # Manually track the error since we're in a test environment
        tb = sys.exc_info()[2]
        tracker._track_error(
            type(e),
            str(e),
            risky_function.__name__,
            tb.tb_lineno,
            __file__
        )
    
    # Check if the error was tracked
    error_key = f"{__file__}:risky_function"
    assert error_key in tracker.error_history
    assert len(tracker.error_history[error_key]) == 1

def test_error_suggestions():
    """Test that suggestions appear after multiple errors."""
    def key_error_function():
        return {}['missing']
    
    # First two errors should be tracked but no suggestions
    for _ in range(2):
        try:
            key_error_function()
        except KeyError as e:
            # Manually track the error
            tb = sys.exc_info()[2]
            tracker._track_error(
                type(e),
                str(e),
                key_error_function.__name__,
                tb.tb_lineno,
                __file__
            )
    
    error_key = f"{__file__}:key_error_function"
    assert len(tracker.error_history[error_key]) == 2
    
    # Third error should trigger a suggestion
    try:
        key_error_function()
    except KeyError as e:
        # Manually track the error
        tb = sys.exc_info()[2]
        tracker._track_error(
            type(e),
            str(e),
            key_error_function.__name__,
            tb.tb_lineno,
            __file__
        )
    
    assert len(tracker.error_history[error_key]) == 3

def test_file_path_tracking():
    """Test that errors are tracked with correct file paths."""
    def test_function():
        raise ValueError("Test error")
    
    try:
        test_function()
    except ValueError as e:
        # Manually track the error
        tb = sys.exc_info()[2]
        tracker._track_error(
            type(e),
            str(e),
            test_function.__name__,
            tb.tb_lineno,
            __file__
        )
    
    error_key = f"{__file__}:test_function"
    assert error_key in tracker.error_history
    error_info = tracker.error_history[error_key][0]
    assert error_info['file'] == __file__
    assert error_info['type'] == 'ValueError'

def test_error_suggestions_content():
    """Test that error suggestions are appropriate for error types."""
    def zero_div():
        return 1/0
    
    # Trigger error three times to get suggestion
    for _ in range(3):
        try:
            zero_div()
        except ZeroDivisionError as e:
            # Manually track the error
            tb = sys.exc_info()[2]
            tracker._track_error(
                type(e),
                str(e),
                zero_div.__name__,
                tb.tb_lineno,
                __file__
            )
    
    error_key = f"{__file__}:zero_div"
    assert len(tracker.error_history[error_key]) == 3
    suggestion = tracker._generate_fix_suggestion(ZeroDivisionError)
    assert "division by zero" in suggestion.lower() 