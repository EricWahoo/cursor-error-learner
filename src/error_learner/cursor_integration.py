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
        self.logger.info("Analyzing current file: %s", file_path)
        return analyzer.analyze_file(file_path)
    
    def analyze_on_save(self, file_path: str) -> None:
        """
        Analyze file when it is saved.
        
        Args:
            file_path: Path to the saved file
        """
        self.logger.info("Analyzing file on save: %s", file_path)
        issues = analyzer.analyze_file(file_path)
        self._report_issues(file_path, issues)
    
    def analyze_on_open(self, file_path: str) -> None:
        """
        Analyze file when it is opened.
        
        Args:
            file_path: Path to the opened file
        """
        self.logger.info("Analyzing file on open: %s", file_path)
        issues = analyzer.analyze_file(file_path)
        self._report_issues(file_path, issues)
    
    def analyze_workspace(self, workspace_path: str) -> None:
        """
        Analyze all Python files in the workspace.
        
        Args:
            workspace_path: Path to the workspace directory
        """
        self.logger.info("Analyzing workspace: %s", workspace_path)
        issues = analyzer.analyze_workspace(workspace_path)
        for file_path, file_issues in issues.items():
            self._report_issues(file_path, file_issues)
    
    def _report_issues(self, file_path: str, issues: List[Dict]) -> None:
        """Report issues found in a file."""
        for issue in issues:
            self.logger.warning(
                "Potential issue in %s at line %d\nType: %s\nMessage: %s\nSuggestion: %s\n",
                file_path,
                issue["line"],
                issue["type"],
                issue["message"],
                issue["suggestion"]
            )

# Create global cursor analyzer instance
cursor_analyzer = CursorAnalyzer() 