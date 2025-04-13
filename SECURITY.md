# Security Policy

## Supported Versions

We release patches for security vulnerabilities for the following versions:

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability within Error Learner, please report it through GitHub's Security Advisory feature. Go to the repository's "Security" tab and click on "Report a vulnerability". All security vulnerabilities will be promptly addressed.

For more information about privately reporting a security vulnerability, see [GitHub's documentation](https://docs.github.com/en/code-security/security-advisories/guidance-on-reporting-and-writing/privately-reporting-a-security-vulnerability).

## Security Measures

Error Learner implements the following security measures:

1. **Error Data Handling**
   - Error data is stored locally and not transmitted to external servers
   - Sensitive information in error messages is not logged

2. **Code Analysis**
   - Static analysis is performed in a sandboxed environment
   - No code execution during analysis

3. **Dependencies**
   - Regular dependency updates
   - Security-focused dependency scanning

4. **Access Control**
   - Local file access only
   - No network operations

## Best Practices

When using Error Learner:

1. Keep the package updated to the latest version
2. Review error logs for sensitive information
3. Use appropriate logging levels in production
4. Regularly check for security updates 