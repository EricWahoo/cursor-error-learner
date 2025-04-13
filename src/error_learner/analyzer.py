"""
Pattern analyzer for identifying potential code issues based on error history.
"""

import ast
import logging
from pathlib import Path
from typing import Dict, List, Set, Optional
from collections import defaultdict

from .extension import tracker

class PatternAnalyzer:
    """Analyzes code patterns and suggests improvements based on error history."""
    
    def __init__(self):
        self.logger = logging.getLogger("error_learner.analyzer")
        self.error_patterns = defaultdict(list)
    
    def analyze_file(self, file_path: str) -> List[Dict]:
        """
        Analyze a Python file for potential issues based on error history.
        
        Args:
            file_path: Path to the Python file to analyze
            
        Returns:
            List of potential issues with suggestions
        """
        try:
            with open(file_path, 'r') as f:
                code = f.read()
            
            tree = ast.parse(code)
            return self._analyze_ast(tree, file_path)
        except Exception as e:
            self.logger.error(f"Error analyzing {file_path}: {e}")
            return []
    
    def _analyze_ast(self, tree: ast.AST, file_path: str) -> List[Dict]:
        """Analyze AST for potential issues."""
        issues = []
        
        # Get error history for this file
        file_errors = self._get_file_errors(file_path)
        
        class NodeVisitor(ast.NodeVisitor):
            def __init__(self, analyzer, file_path, file_errors):
                self.analyzer = analyzer
                self.file_path = file_path
                self.file_errors = file_errors
                self.issues = []
                self.line_offset = 0  # Track line offset for indented code
                self.function_lines = {}  # Map function names to their line numbers
            
            def visit_FunctionDef(self, node):
                """Visit function definitions to track their line numbers."""
                self.function_lines[node.name] = node.lineno
                self.generic_visit(node)
            
            def visit(self, node):
                # Get the line number from the node
                line_no = getattr(node, 'lineno', None)
                if line_no is not None:
                    # Adjust line number for indented code
                    if self.line_offset == 0 and isinstance(node, ast.FunctionDef):
                        # Find the line offset by checking the first function definition
                        self.line_offset = line_no - 2  # Account for the function definition line
                    
                    actual_line = line_no - self.line_offset
                    
                    # Check dictionary access patterns
                    if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Name):
                        self.issues.append({
                            'type': 'KeyError',
                            'line': line_no,
                            'message': f"Potential KeyError: Consider using dict.get() or checking key existence",
                            'suggestion': f"Use dict.get() or check key existence: 'if key in {node.value.id}'"
                        })
                    
                    # Check division operations
                    elif isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
                        self.issues.append({
                            'type': 'ZeroDivisionError',
                            'line': line_no,
                            'message': "Potential division by zero",
                            'suggestion': "Add a check to prevent division by zero"
                        })
                    
                    # Check type-related operations
                    elif isinstance(node, ast.BinOp) and isinstance(node.op, (ast.Add, ast.Sub, ast.Mult)):
                        if any(e['type'] == 'TypeError' for e in self.file_errors):
                            self.issues.append({
                                'type': 'TypeError',
                                'line': line_no,
                                'message': "Potential type mismatch in operation",
                                'suggestion': "Verify types before operation or add type conversion"
                            })
                
                self.generic_visit(node)
        
        visitor = NodeVisitor(self, file_path, file_errors)
        visitor.visit(tree)
        return visitor.issues
    
    def _get_file_errors(self, file_path: str) -> List[Dict]:
        """Get all errors for a specific file."""
        file_errors = []
        for key, errors in tracker.error_history.items():
            # The key format is 'file_path:func_name'
            stored_path = key.split(':')[0] if ':' in key else key
            if stored_path == file_path:
                file_errors.extend(errors)
        return file_errors
    
    def _has_key_errors(self, file_path: str, line_no: int) -> bool:
        """Check if there are KeyErrors at this line."""
        return self._has_error_type(file_path, line_no, 'KeyError')
    
    def _has_zero_division_errors(self, file_path: str, line_no: int) -> bool:
        """Check if there are ZeroDivisionErrors at this line."""
        return self._has_error_type(file_path, line_no, 'ZeroDivisionError')
    
    def _has_type_errors(self, file_path: str, line_no: int) -> bool:
        """Check if there are TypeErrors at this line."""
        return self._has_error_type(file_path, line_no, 'TypeError')
    
    def _has_error_type(self, file_path: str, line_no: int, error_type: str) -> bool:
        """Check if a specific type of error exists at a line."""
        errors = self._get_file_errors(file_path)
        return any(
            e['type'] == error_type and e['line'] == line_no
            for e in errors
        )
    
    def analyze_workspace(self, workspace_path: str) -> Dict[str, List[Dict]]:
        """
        Analyze all Python files in a workspace.
        
        Args:
            workspace_path: Path to the workspace directory
            
        Returns:
            Dictionary mapping file paths to lists of potential issues and errors
        """
        workspace = Path(workspace_path)
        issues = {}
        
        for py_file in workspace.rglob('*.py'):
            if not any(ignore in str(py_file) for ignore in ['.venv', '__pycache__', '.git']):
                file_path = str(py_file)
                print(f"Analyzing file: {file_path}")  # Debug
                file_issues = self.analyze_file(file_path)
                file_errors = self._get_file_errors(file_path)
                print(f"Found errors: {file_errors}")  # Debug
                print(f"Found issues: {file_issues}")  # Debug
                
                # Include file if it has either errors or issues
                if file_errors or file_issues:
                    # Convert file errors to issue format
                    error_issues = [{
                        'type': error['type'],
                        'message': f"Previous {error['type']} occurred here",
                        'line': error['line'],
                        'suggestion': "Consider adding error handling"
                    } for error in file_errors]
                    
                    # Combine both errors and issues
                    issues[file_path] = error_issues + file_issues
                    print(f"Added to issues: {issues[file_path]}")  # Debug
        
        print(f"Final issues: {issues}")  # Debug
        return issues

# Create global analyzer instance
analyzer = PatternAnalyzer() 