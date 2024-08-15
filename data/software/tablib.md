# Tablib: Tabular Datasets

Tablib is a format-agnostic tabular dataset library, written in Python. It allows you to import, export, and manipulate tabular data sets.

## Features

- **Format Agnostic**: Tablib supports a variety of formats, including Excel, CSV, JSON, and YAML, allowing you to work with data in different file types.
- **Data Manipulation**: The library provides functions for sorting, filtering, and transforming data sets, enabling you to perform common data operations.
- **Import and Export**: Tablib allows you to import data from files or URLs, and export data to different formats, making it easy to work with data from various sources.

This was one of my first open source projects. The [documentation](https://tablib.readthedocs.io/en/stable/) is extensive and covers all aspects of the library. It was my passion project for a long time.

## Installation

You can install Tablib using pip:

```bash
$ pip install tablib
```

## Documentation

The official documentation for Tablib can be found [here](https://tablib.readthedocs.io/en/stable/).

## Usage

Here's an example of how you can use Tablib to work with tabular datasets in Python:

```python
import tablib

# Create a dataset
data = tablib.Dataset(headers=["Name", "Age", "City"])
for row in [
    ["Alice", 24, "New York"],
    ["Bob", 30, "San Francisco"],
    ["Charlie", 28, "Seattle"],
]:
    data.append(row)
