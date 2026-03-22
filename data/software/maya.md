# Maya: Datetimes for Humans

Maya makes datetimes easy in Python. No more guessing which datetime class to use, no more timezone bugs at 2am, no more Googling strftime format codes for the hundredth time.

    $ uv pip install maya

## What It Looks Like

```python
import maya

# Get the current time.
now = maya.now()
print(now)
# <MayaDT epoch=1711100000.0>

# Parse anything.
maya.parse("2024-01-15")
maya.parse("January 15th, 2024")
maya.parse("tomorrow")
maya.parse("2 hours ago")

# Format for humans.
now.slang_date()
# 'today'

now.slang_time()
# 'just now'

# RFC 2822 for email headers.
now.rfc2822()
# 'Sat, 22 Mar 2026 12:00:00 GMT'

# ISO 8601 for APIs.
now.iso8601()
# '2026-03-22T12:00:00Z'

# Convert between timezones.
now.datetime(to_timezone="US/Eastern")
```

No timezone confusion. No naive vs. aware datetime headaches. Maya handles it all internally and gives you the right answer.

## The Philosophy

Python's built-in datetime module is powerful and precise. It is also confusing. The distinction between naive and aware datetimes has tripped up every Python developer at least once. Timezone handling requires importing three different modules. Parsing a simple date string takes more code than it should.

Maya wraps all of that complexity in an interface that matches how humans actually think about time. "Tomorrow" is a valid input. "2 hours ago" works. The library figures out what you mean and gives you a reliable result.

Named after the Maya civilization, whose calendar systems were among the most sophisticated in human history. They understood time deeply. This library tries to make that understanding accessible.

## Install

```bash
$ uv pip install maya
```

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/maya)
- [Python Package Index](https://pypi.org/project/maya/)

## Related

- [**Requests**](/software/requests) — The "for humans" philosophy that started it all.
- [**Tablib**](/software/tablib) — Another library built on the principle that APIs should fit in your head.
