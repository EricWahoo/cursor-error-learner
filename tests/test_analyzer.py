"""
Tests for the pattern analyzer functionality.
"""

import pytest
import tempfile
import os
from error_learner.analyzer import analyzer
from error_learner.extension import tracker

def test_pattern_analysis():
    """Test that the analyzer can identify potential issues."""
    # Create a temporary Python file with potential issues
    code = """
def process_data(data):
    # This might raise KeyError
    value = data['key']
    
    # This might raise ZeroDivisionError
    result = 100 / value
    
    # This might raise TypeError
    return result + "10"
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py') as f:
        f.write(code)
        f.flush()
        
        # Simulate some errors
        try:
            # KeyError
            exec(f"data = {{}}\nvalue = data['key']", {}, {})
        except KeyError as e:
            tracker._track_error(type(e), str(e), 'process_data', 3, f.name)
        
        try:
            # ZeroDivisionError
            exec('result = 100 / 0', {}, {})
        except ZeroDivisionError as e:
            tracker._track_error(type(e), str(e), 'process_data', 6, f.name)
        
        try:
            # TypeError
            exec('x = 10 + "10"', {}, {})
        except TypeError as e:
            tracker._track_error(type(e), str(e), 'process_data', 9, f.name)
        
        # Analyze the file
        issues = analyzer.analyze_file(f.name)
        
        # Check that all issues were identified
        assert len(issues) == 3
        
        # Check KeyError detection
        key_issues = [i for i in issues if i['type'] == 'KeyError']
        assert len(key_issues) == 1
        assert 'dict.get()' in key_issues[0]['suggestion']
        
        # Check ZeroDivisionError detection
        div_issues = [i for i in issues if i['type'] == 'ZeroDivisionError']
        assert len(div_issues) == 1
        assert 'division by zero' in div_issues[0]['message'].lower()
        
        # Check TypeError detection
        type_issues = [i for i in issues if i['type'] == 'TypeError']
        assert len(type_issues) == 1
        assert 'type mismatch' in type_issues[0]['message'].lower()

def test_workspace_analysis():
    """Test analyzing an entire workspace."""
    with tempfile.TemporaryDirectory() as workspace:
        # Create a Python file with issues
        code = """
def risky_function():
    data = {}
    return data['missing'] / 0
"""
        file_path = os.path.join(workspace, 'test.py')
        with open(file_path, 'w') as f:
            f.write(code)
        
        # Simulate an error
        try:
            exec(code, {}, {})
        except KeyError as e:
            tracker._track_error(type(e), str(e), 'risky_function', 3, file_path)
        
        # Analyze workspace
        issues = analyzer.analyze_workspace(workspace)
        
        # Check results
        assert file_path in issues
        assert len(issues[file_path]) > 0
        assert any(i['type'] == 'KeyError' for i in issues[file_path]) 