# Error Learner

A Python tool for tracking and learning from errors in your code. This package provides functionality to automatically track errors, analyze patterns, and suggest fixes based on error history.

## Features

- 🎯 Automatic error tracking with a simple decorator
- 📊 Error statistics and analysis
- 💡 Smart fix suggestions after multiple occurrences
- 🔍 Proactive issue detection in code analysis
- 🌍 Workspace-wide code analysis
- 📝 Detailed error information including timestamps and context
- 🚀 Command-line interface for error analysis

## Requirements

- Python 3.9 or higher
- pip (Python package installer)

## Installation

```bash
# Clone the repository
git clone https://github.com/EricWahoo/cursor-error-learner.git
cd cursor-error-learner

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package in development mode
pip install -e .

# For development, install additional dependencies
pip install -e ".[dev]"
```

## Usage

### Basic Usage

```python
from error_learner import track

@track
def your_function():
    # Your code here
    pass
```

### Error Tracking Example

```python
from error_learner import track

@track
def divide_numbers(a, b):
    return a / b

# First run - error is tracked
try:
    divide_numbers(1, 0)
except ZeroDivisionError:
    pass

# After multiple occurrences, fix suggestions are provided
```

### Code Analysis Example

```python
from error_learner import analyzer

# Analyze a single file
issues = analyzer.analyze_file('your_script.py')
for issue in issues:
    print(f"Line {issue['line']}: {issue['message']}")
    print(f"Suggestion: {issue['suggestion']}")

# Analyze entire workspace
workspace_issues = analyzer.analyze_workspace('your_project_dir')
for file_path, file_issues in workspace_issues.items():
    print(f"\nIssues in {file_path}:")
    for issue in file_issues:
        print(f"Line {issue['line']}: {issue['message']}")
```

### CLI Usage

```bash
# Get error statistics
error-learner stats

# Get stats for a specific function
error-learner stats --function your_function_name

# Analyze a Python file
error-learner analyze your_script.py

# Analyze entire workspace
error-learner analyze --workspace your_project_dir

# Set log level
error-learner --log-level DEBUG stats
```

## Development

### Setup Development Environment

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Project Structure

```
cursor-error-learner/
├── src/
│   └── error_learner/
│       ├── __init__.py
│       ├── analyzer.py      # Pattern analysis and workspace scanning
│       ├── core.py         # Core error tracking functionality
│       ├── extension.py    # Cursor IDE integration
│       └── utils.py        # Utility functions
├── tests/
│   ├── __init__.py
│   ├── test_analyzer.py
│   ├── test_core.py
│   ├── test_demo.py
│   └── test_extension.py
├── .gitignore
├── CHANGELOG.md
├── README.md
├── setup.py
└── pytest.ini
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.