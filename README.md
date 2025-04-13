# Error Learner

A Python tool for tracking and learning from errors in your code. This package provides functionality to automatically track errors, analyze patterns, and suggest fixes based on error history. It integrates seamlessly with the Cursor IDE for enhanced development experience.

## Features

- 🎯 Automatic error tracking with zero configuration in Cursor IDE
- 📊 Real-time error statistics and analysis
- 💡 Smart fix suggestions after recurring errors
- 🔍 Proactive issue detection through static code analysis
- 🌍 Workspace-wide code pattern analysis
- 📝 Detailed error tracking with timestamps and context
- 🚀 Rich command-line interface for error analysis
- 🔒 Secure local-only error tracking
- 🎨 Beautiful console output with rich formatting

## Requirements

- Python 3.9 or higher
- pip (Python package installer)
- Cursor IDE (for automatic integration)

## Installation

```bash
# Install directly from GitHub
pip install git+https://github.com/EricWahoo/cursor-error-learner.git

# For development features
pip install git+https://github.com/EricWahoo/cursor-error-learner.git#egg=cursor-error-learner[dev]
```

## Quick Start

Error Learner works automatically in Cursor IDE! Just install the package and start coding. For manual integration:

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

# Errors are automatically tracked
try:
    divide_numbers(1, 0)
except ZeroDivisionError:
    pass

# After 3 occurrences, you'll get fix suggestions
```

### Code Analysis Example

```python
from error_learner import analyzer

# Analyze current file
issues = analyzer.analyze_file('your_script.py')
for issue in issues:
    print(f"Line {issue['line']}: {issue['message']}")
    print(f"Suggestion: {issue['suggestion']}")

# Analyze workspace
workspace_issues = analyzer.analyze_workspace('.')
for file_path, file_issues in workspace_issues.items():
    print(f"\nIssues in {file_path}:")
    for issue in file_issues:
        print(f"Line {issue['line']}: {issue['message']}")
```

### CLI Usage

```bash
# View error statistics
error-learner stats

# Analyze current directory
error-learner analyze .

# Analyze specific file
error-learner analyze path/to/file.py

# Get detailed help
error-learner --help
```

## Security

Error Learner takes security seriously:
- All error data is stored locally
- No external API calls or data transmission
- Sensitive information is automatically redacted from error logs
- See SECURITY.md for our full security policy

## Development

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/EricWahoo/cursor-error-learner.git
cd cursor-error-learner

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all extras
pip install -e ".[dev]"

# Run tests with coverage
pytest --cov=src/error_learner
```

### Project Structure

```
cursor-error-learner/
├── src/
│   └── error_learner/
│       ├── __init__.py      # Package initialization and exports
│       ├── analyzer.py      # Pattern analysis and code scanning
│       ├── core.py         # Core error tracking functionality
│       ├── extension.py    # Cursor IDE integration
│       ├── utils.py        # Utility functions
│       └── cli.py         # Command-line interface
├── tests/                 # Comprehensive test suite
├── examples/             # Usage examples
├── docs/                # Documentation
└── [configuration files]
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Built with ❤️ for the Cursor IDE community
- Special thanks to all contributors