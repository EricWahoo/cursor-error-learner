"""
Tests for the Cursor integration module.
"""

import pytest
import logging
from pathlib import Path
from error_learner.cursor_integration import CursorAnalyzer

@pytest.fixture
def cursor_analyzer():
    """Create a CursorAnalyzer instance for testing."""
    analyzer = CursorAnalyzer()
    analyzer.logger.setLevel(logging.INFO)
    return analyzer

def test_analyze_current_file(cursor_analyzer, tmp_path):
    """Test analyzing the current file."""
    # Create a test file
    test_file = tmp_path / "test.py"
    test_file.write_text("def test():\n    return 1/0")
    
    issues = cursor_analyzer.analyze_current_file(str(test_file))
    assert len(issues) > 0
    assert any(issue["type"] == "ZeroDivisionError" for issue in issues)

def test_analyze_on_save(cursor_analyzer, tmp_path, caplog):
    """Test analyzing on file save."""
    caplog.set_level(logging.INFO)
    test_file = tmp_path / "test.py"
    test_file.write_text("def test():\n    return 1/0")
    
    cursor_analyzer.analyze_on_save(str(test_file))
    assert any("Analyzing file on save" in record.message for record in caplog.records)
    assert any("Potential issue" in record.message for record in caplog.records)

def test_analyze_on_open(cursor_analyzer, tmp_path, caplog):
    """Test analyzing on file open."""
    caplog.set_level(logging.INFO)
    test_file = tmp_path / "test.py"
    test_file.write_text("def test():\n    return 1/0")
    
    cursor_analyzer.analyze_on_open(str(test_file))
    assert any("Analyzing file on open" in record.message for record in caplog.records)
    assert any("Potential issue" in record.message for record in caplog.records)

def test_analyze_workspace(cursor_analyzer, tmp_path, caplog):
    """Test analyzing entire workspace."""
    caplog.set_level(logging.INFO)
    # Create a test workspace
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    (workspace / "test1.py").write_text("def test1():\n    return 1/0")
    (workspace / "test2.py").write_text("def test2():\n    return 1/0")
    
    cursor_analyzer.analyze_workspace(str(workspace))
    assert any("Analyzing workspace" in record.message for record in caplog.records)
    assert len([r for r in caplog.records if "Potential issue" in r.message]) == 2 