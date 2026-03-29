# Requests: HTTP for Humans

Requests is the most downloaded Python package on Earth. Over 30 million installs a day. It exists because urllib2 was hostile to humans, and HTTP shouldn't be.

    $ uv pip install requests

## What It Looks Like

```python
import requests

# GET a webpage.
r = requests.get("https://api.github.com/user", auth=("user", "pass"))

print(r.status_code)
# 200

print(r.headers["content-type"])
# 'application/json; charset=utf-8'

print(r.json())
# {'login': 'user', 'id': 123456, ...}
```

That's it. No handlers. No openers. No abstractions between you and the thing you're trying to do.

## Before Requests

This is what HTTP looked like in Python before Requests existed:

```python
import urllib2
import base64

request = urllib2.Request("https://api.github.com/user")
base64string = base64.b64encode("%s:%s" % ("user", "pass"))
request.add_header("Authorization", "Basic %s" % base64string)

try:
    result = urllib2.urlopen(request)
    print result.getcode()
    print result.read()
except urllib2.URLError, e:
    print e
```

Seven lines of ceremony to do what Requests does in one. Three imports. Manual base64 encoding for basic auth. An exception hierarchy that tells you what went wrong but not how to fix it. The interface told your subconscious "this is hard" before you'd accomplished anything.

## The Philosophy

Requests was built on a simple conviction: **if you're making the developer feel stupid, the problem is your API, not your developer.**

```python
# POST with JSON data.
r = requests.post("https://httpbin.org/post", json={"key": "value"})

# Upload a file.
r = requests.post("https://httpbin.org/post", files={"file": open("report.csv", "rb")})

# Set a timeout. Because hanging forever is not a feature.
r = requests.get("https://api.example.com/slow", timeout=5)

# Sessions persist cookies across requests.
s = requests.Session()
s.get("https://httpbin.org/cookies/set/session/value")
r = s.get("https://httpbin.org/cookies")
print(r.json())
# {'cookies': {'session': 'value'}}

# Custom headers.
r = requests.get("https://api.example.com/data", headers={"Accept": "application/xml"})

# SSL verification on by default. Because security shouldn't be opt-in.
r = requests.get("https://example.com")
# ✓ SSL certificate verified automatically.
```

Every method does what you'd expect. Every default is sensible. Every error message tells you what happened and what to do about it. The API fits in your head because it was designed to fit in your head.

## What It Taught Me

I was twenty-one when I wrote the first version of Requests. I had no degree, no credentials, no professional network. I was [working at McDonald's](/essays/2026-03-06-the_coworking_space_saved_my_life) the year before. The library became the standard because it solved a real problem simply, and the community recognized it.

That experience became the foundation for everything I've built since. The "for humans" philosophy started as API design and became a [life philosophy](/essays/2025-08-27-from_http_to_consciousness). It shaped how I think about [marriage](/essays/2026-03-06-what_requests_taught_me_about_marriage), [mental health tools](/essays/2026-03-18-designing_for_the_worst_day), [Bible study applications](/software/kjvstudy), and [what we owe each other when we build things people think through](/essays/2026-03-20-the_interface_is_the_subconscious).

It also [nearly broke me](/essays/2026-03-18-open_source_gave_me_everything_until_i_had_nothing_left_to_give). The same intensity that produced Requests produced the conditions for my worst mental health crises. The engine was the same. It just had two outputs.

**Fun fact**: the Requests logo is a [tattoo on my right arm](/photography/tattoos).

## Install

```bash
$ uv pip install requests
```

## Resources

- [Documentation](https://docs.python-requests.org/)
- [Source Code on GitHub](https://github.com/psf/requests)
- [Python Package Index](https://pypi.org/project/requests/)

## Related

- [**The Lego Bricks Era**](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed) — The golden era of open source that produced Requests.
- [**Designing for the Worst Day**](/essays/2026-03-18-designing_for_the_worst_day) — The design philosophy that started here.
- [**The Maintainer Is the Interface**](/essays/2026-03-22-the_maintainer_is_the_interface) — What maintaining Requests taught me about human interfaces.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — How "for humans" became a worldview.
