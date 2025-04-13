# Error Learner

A Python tool for tracking and learning from errors in your code. This package provides functionality to automatically track errors, analyze patterns, and suggest fixes based on error history.

## Features

- 🎯 Automatic error tracking with a simple decorator
- 📊 Error statistics and analysis
- 💡 Smart fix suggestions after multiple occurrences
- 📝 Detailed error information including timestamps and context
- 🚀 Command-line interface for error analysis

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cursor-error-learner.git
cd cursor-error-learner

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the package
pip install -e .
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

### Example

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

### CLI Usage

```bash
# Get error statistics
error-learner stats

# Get stats for a specific function
error-learner stats --function your_function_name

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
│       ├── core.py
│       └── utils.py
├── cli/
│   └── cli.py
├── tests/
│   ├── __init__.py
│   └── test_core.py
├── .gitignore
├── README.md
├── setup.py
└── requirements.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.