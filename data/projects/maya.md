# Maya: Datetimes for Humans

Maya is a Python library that simplifies working with datetimes. It provides a simple and intuitive interface for parsing, formatting, and manipulating dates and times, making it easier to work with temporal data in Python.

## Features

- **Human-readable API**: Maya's API is designed to be easy to read and understand, making it simple to work with datetimes in Python.
- **Timezone support**: Maya supports working with datetimes in different timezones, allowing you to handle time conversions and daylight saving time changes.
- **Parsing and formatting**: Maya provides functions for parsing datetimes from strings and formatting datetimes to strings, making it easy to work with date and time data.
- **Manipulation**: Maya allows you to manipulate datetimes by adding or subtracting time intervals, such as days, hours, minutes, and seconds.
- **Relative datetimes**: Maya supports working with relative datetimes, such as "tomorrow," "next week," or "last month," making it easy to work with dates in a human-friendly way.

## Installation

You can install Maya using pip:

```bash
$ pip install maya
```

## Usage

Here's an example of how you can use Maya to work with datetimes in Python:

```python
import maya

# Create a datetime object
dt = maya.now()

# Format the datetime as a string
formatted_dt = dt.rfc2822()

print(formatted_dt)
```
