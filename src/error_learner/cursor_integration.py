"""
Cursor integration for code analysis and error pattern detection.
"""

import json
import logging
from pathlib import Path
from typing import Dict, List, Any

from .analyzer import analyzer
from .extension import tracker

class CursorAnalyzer:
    """Integrates error pattern analysis with Cursor's code analysis."""
    
    def __init__(self):
        self.logger = logging.getLogger("error_learner.cursor")
    
    def analyze_current_file(self, file_path: str) -> List[Dict]:
        """
        Analyze the current file in Cursor.
        
        Args:
            file_path: Path to the current file
            
        Returns:
            List of potential issues with suggestions
        """
        return analyzer.analyze_file(file_path)
    
    def analyze_on_save(self, file_path: str) -> None:
        """
        Analyze file when it's saved in Cursor.
        
        Args:
            file_path: Path to the saved file
        """
        issues = self.analyze_current_file(file_path)
        if issues:
            self._report_issues(file_path, issues)
    
    def analyze_on_open(self, file_path: str) -> None:
        """
        Analyze file when it's opened in Cursor.
        
        Args:
            file_path: Path to the opened file
        """
        issues = self.analyze_current_file(file_path)
        if issues:
            self._report_issues(file_path, issues)
    
    def analyze_workspace(self, workspace_path: str) -> None:
        """
        Analyze entire workspace in Cursor.
        
        Args:
            workspace_path: Path to the workspace
        """
        issues = analyzer.analyze_workspace(workspace_path)
        for file_path, file_issues in issues.items():
            self._report_issues(file_path, file_issues)
    
    def _report_issues(self, file_path: str, issues: List[Dict]) -> None:
        """Report issues to Cursor's diagnostic panel."""
        for issue in issues:
            self.logger.warning(
                f"Potential issue in {file_path} at line {issue['line']}\n"
                f"Type: {issue['type']}\n"
                f"Message: {issue['message']}\n"
                f"Suggestion: {issue['suggestion']}\n"
            )

# Create global cursor analyzer instance
cursor_analyzer = CursorAnalyzer() 