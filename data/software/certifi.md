# Certifi: Python's Trust Store

Certifi provides Mozilla's carefully curated CA certificate bundle for Python. It exists because SSL verification in Python was broken, and security shouldn't require a PhD in certificate management.

    $ uv pip install certifi

## What It Looks Like

```python
import certifi

# Get the path to the CA bundle.
certifi.where()
# '/path/to/certifi/cacert.pem'

# Use it with Requests (this happens automatically).
import requests
requests.get("https://example.com", verify=certifi.where())

# Or with urllib3 directly.
import urllib3
http = urllib3.PoolManager(ca_certs=certifi.where())
r = http.request("GET", "https://example.com")

# Or with the standard library.
import ssl
ctx = ssl.create_default_context(cafile=certifi.where())
```

That's the entire API. One function. One return value. One job done well.

## Why It Matters

Before Certifi, Python's SSL story was a mess. Every operating system stored certificates differently. macOS had the Keychain. Linux distributions scattered them across `/etc/ssl/`, `/etc/pki/`, or wherever they felt like it. Windows did its own thing entirely. The result: developers disabled SSL verification just to get their code working. Security became opt-in, which effectively meant opt-out.

Certifi solved this by bundling Mozilla's trusted CA certificates directly into a Python package. Same certificates on every platform, always up to date, always available. Over 70 million downloads per month. It ships as a dependency of [Requests](/software/requests), which means most Python applications that talk to the internet are trusting Certifi to keep that conversation private.

## The Invisible Infrastructure

I built Certifi because [Requests](/software/requests) needed a way to verify SSL certificates that actually worked everywhere. The alternative was telling users to figure out their system's certificate store, which is exactly the kind of "your problem, not mine" attitude I was trying to eliminate from Python's HTTP story.

The best infrastructure is the kind you never think about. Certifi works so well that developers forget it exists, which is exactly the point. It's a single function that returns a file path, and that file path makes the entire Python ecosystem more secure by default.

There's a lesson in that. Sometimes the most impactful work is the least visible. No one writes blog posts about their CA certificate bundle. But every `requests.get("https://...")` call that silently succeeds is Certifi doing its job.

## Install

```bash
$ uv pip install certifi
```

## Resources

- [Source Code on GitHub](https://github.com/certifi/python-certifi)
- [Python Package Index](https://pypi.org/project/certifi/)
- [Mozilla CA Certificate Program](https://wiki.mozilla.org/CA)

## Related

- [**Requests**](/software/requests) — The HTTP library that depends on Certifi for SSL verification.
- [**Designing for the Worst Day**](/essays/2026-03-18-designing_for_the_worst_day) — Security defaults as a form of compassionate design.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — The "for humans" philosophy means secure by default.
