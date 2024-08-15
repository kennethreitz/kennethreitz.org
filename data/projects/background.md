# background

`background` is a simple program that allows you to run background tasks
in any Python application. It is a simple and easy-to-use library that
allows you to run tasks in the background without blocking the main
thread.

I'm using it on this FastAPI application to run trivial background tasks,
outside of the main event loop.


## Installation

You can install `background` using `pip`:

```bash
$ uv pip install background
```

## Usage

Here is a simple example of how you can use `background`:

```python
import time
import background

@background.task
def work():
    # Do something expensive here.
    time.sleep(10)


for _ in range(100):
    work()
```

The repository was gifted to [Parth Shandilya](https://github.com/ParthS007),
who now maintains the project.

## Learn More


https://github.com/ParthS007/background
