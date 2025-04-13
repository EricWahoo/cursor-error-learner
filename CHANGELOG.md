# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2024-04-14

### Added
- Proactive issue detection in code analysis
- Support for analyzing entire workspaces
- Debug logging for better troubleshooting

### Changed
- Improved pattern analysis to detect potential issues before errors occur
- Enhanced workspace analysis to include both errors and potential issues
- Optimized error tracking with better file path handling

### Fixed
- Fixed workspace analysis not detecting files with potential issues
- Improved error key format handling in file error tracking
- Removed unnecessary error history checks for certain error types

## [1.0.0] - 2024-04-13

### Added
- Initial release of Error Learner
- Core error tracking functionality with `@track` decorator
- Error analysis and fix suggestions
- Command-line interface for error statistics
- Comprehensive test suite
- Documentation and examples

### Changed
- Project structure optimized for production use
- Code organization following Python best practices
- Type hints and docstrings added throughout
- Error tracking logic improved for better suggestions

### Fixed
- Initial project setup and packaging
- Development environment configuration
- Test coverage and quality 