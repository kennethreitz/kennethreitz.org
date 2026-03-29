# Background: Simple Background Tasks

Background lets you run Python functions in background threads with a single decorator. No task queue. No message broker. No configuration. Just `@background.task` and you're done.

    $ uv add background

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

Under the hood, Background uses a `ThreadPoolExecutor`. The default thread count matches your CPU cores. You can configure it if you need to:

```python
import background

# Set the number of background threads.
background.n = 8

@background.task
def process_image(path):
    # Up to 8 of these will run concurrently.
    resize_and_compress(path)

# Returns a Future you can inspect if needed.
future = process_image("/uploads/photo.jpg")
future.result()  # Block until complete, if you want.
```

The decorated function returns a `concurrent.futures.Future`, so you get the simplicity of fire-and-forget with the option to wait for results when you need them.

## The Philosophy

Sometimes you need Celery. Sometimes you need Redis and a message broker and dead-letter queues and retry policies. And sometimes you just need a function to run without blocking the main thread. Background is for that third case.

Not everything needs infrastructure. Not every background task needs to survive a server restart. Sometimes a thread pool and a decorator are exactly enough. The gap between "I need this to run in the background" and "I need a distributed task queue" is enormous, and Background lives in that gap.

I use it on this very website for trivial background tasks outside the main event loop. It's the kind of tool that would be embarrassing to over-engineer and satisfying to keep simple.

The project was gifted to [Parth Shandilya](https://github.com/ParthS007), who now maintains it.

## Install

```bash
$ uv add background
```

## Resources

- [Source Code on GitHub](https://github.com/ParthS007/background)
- [Python Package Index](https://pypi.org/project/background/)

## Related

- [**Delegator**](/software/delegator) — Another small, focused utility for common Python tasks.
- [**Requests**](/software/requests) — The philosophy that simple tools should stay simple.
- [**Programming as Spiritual Practice**](/essays/2025-08-26-programming_as_spiritual_practice) — Knowing when not to over-engineer is its own discipline.
