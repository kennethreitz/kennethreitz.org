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

# Convert between timezones without losing your mind.
now.datetime(to_timezone="US/Eastern")
now.datetime(to_timezone="Europe/London")
now.datetime(to_timezone="Asia/Tokyo")

# Generate ranges of time.
start = maya.when("2024-01-01")
end = maya.when("2024-01-31")
for day in maya.intervals(start=start, end=end, interval=60*60*24):
    print(day.slang_date())
```

No timezone confusion. No naive vs. aware datetime headaches. Maya handles it all internally and gives you the right answer.

## The Philosophy

Python's built-in datetime module is powerful and precise. It is also confusing. The distinction between naive and aware datetimes has tripped up every Python developer at least once. Timezone handling requires importing three different modules. Parsing a simple date string takes more code than it should.

Maya wraps all of that complexity in an interface that matches how humans actually think about time. "Tomorrow" is a valid input. "2 hours ago" works. The library figures out what you mean and gives you a reliable result.

## The Name

Named after the Maya civilization, whose calendar systems were among the most sophisticated in human history. They tracked cycles within cycles — the 260-day Tzolkʼin, the 365-day Haabʼ, the Long Count spanning millennia. They understood time deeply, not as a flat line but as interlocking patterns.

This library tries to make that kind of understanding accessible. Not the complexity, but the confidence. When you work with Maya, you can trust that the timezone is right, the format is correct, and the edge cases are handled. You think about time the way you naturally think about time, and the library does the rest.

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
- [**Programming as Spiritual Practice**](/essays/2025-08-26-programming_as_spiritual_practice) — The contemplative approach to building tools that respect their users.
