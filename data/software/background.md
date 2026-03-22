# Background: Simple Background Tasks

Background lets you run Python functions in background threads with a single decorator. No task queue. No message broker. No configuration. Just `@background.task` and you're done.

    $ uv pip install background

## What It Looks Like

```python
import time
import background

@background.task
def send_email(to, subject, body):
    # This runs in a background thread.
    time.sleep(2)  # Simulate sending.
    print(f"Sent '{subject}' to {to}")

# These all return immediately.
send_email("alice@example.com", "Hello", "How are you?")
send_email("bob@example.com", "Update", "Project shipped.")
send_email("charlie@example.com", "Reminder", "Meeting at 3.")

# Main thread keeps running while emails send in the background.
print("All emails queued.")
```

Under the hood, Background uses a `ThreadPoolExecutor`. The default thread count matches your CPU cores. You can configure it if you need to.

## The Philosophy

Sometimes you need Celery. Sometimes you need Redis. And sometimes you just need a function to run without blocking the main thread. Background is for that third case.

I use it on this very website for trivial background tasks outside the main event loop. Not everything needs infrastructure. Sometimes a thread pool and a decorator are exactly enough.

The project was gifted to [Parth Shandilya](https://github.com/ParthS007), who now maintains it.

## Install

```bash
uv pip install background
```

## Resources

- [Source Code on GitHub](https://github.com/ParthS007/background)
- [Python Package Index](https://pypi.org/project/background/)

## Related

- [**Delegator**](/software/delegator) — Another small, focused utility for common Python tasks.
- [**Requests**](/software/requests) — The philosophy that simple tools should stay simple.
