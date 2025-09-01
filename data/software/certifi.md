# Certifi: Trust Database for Humans

Certifi is a Python library that provides Mozilla's CA Bundle in a simple, trustworthy format. It was born from the frustration of SSL certificate verification problems that plagued Python developers.

    $ uv pip install certifi

The library solves a fundamental infrastructure problem: Python's SSL certificate verification needed a reliable, up-to-date source of trusted Certificate Authorities. Rather than relying on system-specific certificate stores that varied wildly between operating systems, Certifi provides Mozilla's curated CA bundle in a format Python can use.

This project is downloaded over 70 million times per month, making it one of the most critical pieces of Python security infrastructure. It's a dependency for Requests and countless other libraries that handle HTTPS connections.

## The Problem It Solved

Before Certifi, Python developers faced constant SSL verification headaches:

- Different certificate stores on different systems
- Outdated or missing CA bundles
- Complex, system-specific configuration
- Security vulnerabilities from disabled verification

## The "For Humans" Approach

Like [Requests](/software/requests), Certifi follows the "For Humans" philosophy:

- **Reliable**: Always-updated Mozilla CA bundle
- **Consistent**: Same behavior across all platforms  
- **Simple**: One import, one function call
- **Secure**: Verification on by default

```python
import certifi
certifi.where()  # Returns the path to the CA bundle
```

## Impact

Certifi became invisible infrastructure that millions of Python applications depend on. It's the kind of utility that, when it works correctly, nobody thinks about it—which is exactly how good infrastructure should be.

The success of Certifi demonstrates how solving fundamental problems with simple, reliable tools can have massive impact across the entire ecosystem.

## Resources

- [Certifi on PyPI](https://pypi.org/project/certifi/)
- [Mozilla CA Certificate Program](https://wiki.mozilla.org/CA)
- [Python SSL Documentation](https://docs.python.org/3/library/ssl.html)

## Philosophy

> Sometimes the most important code is the most boring code. Certifi does one thing well: provides a trusted source of CA certificates. It's infrastructure that works so well that developers forget it exists—until it saves them from security vulnerabilities they never knew they had.