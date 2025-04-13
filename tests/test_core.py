"""
Tests for the core error tracking functionality.
"""

import pytest
from datetime import datetime
from error_learner.core import ErrorTracker, track, ErrorInfo, _tracker

@pytest.fixture
def tracker():
    """Fixture providing a fresh ErrorTracker instance."""
    return ErrorTracker()

def test_track_decorator(tracker):
    """Test that the track decorator properly tracks errors."""
    @tracker.track
    def error_function():
        raise ValueError("Test error")
    
    with pytest.raises(ValueError):
        error_function()
    
    assert "error_function" in tracker.error_history
    assert len(tracker.error_history["error_function"]) == 1
    
    error_info = tracker.error_history["error_function"][0]
    assert isinstance(error_info, ErrorInfo)
    assert error_info.error_type == ValueError
    assert error_info.error_message == "Test error"
    assert error_info.function_name == "error_function"

def test_error_analysis(tracker):
    """Test that error analysis suggests fixes after multiple occurrences."""
    @tracker.track
    def divide_by_zero():
        return 1/0
    
    # First two errors should not have suggestions
    for _ in range(2):
        with pytest.raises(ZeroDivisionError):
            divide_by_zero()
    
    assert tracker.error_history["divide_by_zero"][0].fix_suggestion is None
    assert tracker.error_history["divide_by_zero"][1].fix_suggestion is None
    
    # Third error should have a suggestion
    with pytest.raises(ZeroDivisionError):
        divide_by_zero()
    
    assert tracker.error_history["divide_by_zero"][2].fix_suggestion is not None
    assert "denominator" in tracker.error_history["divide_by_zero"][2].fix_suggestion.lower()

def test_global_tracker():
    """Test that the global tracker works correctly."""
    @track
    def test_function():
        raise KeyError("Missing key")
    
    with pytest.raises(KeyError):
        test_function()
    
    # The global tracker should have recorded the error
    assert "test_function" in _tracker.error_history 