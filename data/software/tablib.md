# Tablib: Tabular Datasets for Humans

Tablib is a format-agnostic tabular dataset library for Python. Create a dataset once, export it to CSV, JSON, Excel, YAML, or a pandas DataFrame. The data stays the same. The format is up to you.

    $ uv add tablib

## What It Looks Like

```python
import tablib

# Create a dataset.
data = tablib.Dataset(headers=["Name", "Age", "City"])

data.append(["Alice", 28, "Portland"])
data.append(["Bob", 34, "Seattle"])
data.append(["Charlie", 22, "Austin"])

# Export to CSV.
print(data.export("csv"))
# Name,Age,City
# Alice,28,Portland
# Bob,34,Seattle
# Charlie,22,Austin

# Export to JSON.
print(data.export("json"))
# [{"Name": "Alice", "Age": 28, "City": "Portland"}, ...]

# Export to Excel.
with open("people.xlsx", "wb") as f:
    f.write(data.export("xlsx"))

# Import from CSV.
data = tablib.Dataset().load(open("people.csv").read())

# Filter columns dynamically.
print(data["Name"])
# ['Alice', 'Bob', 'Charlie']

# Stack datasets together.
more_people = tablib.Dataset(headers=["Name", "Age", "City"])
more_people.append(["Diana", 29, "Denver"])
combined = data.stack(more_people)

# Databooks: multiple sheets in one export.
book = tablib.Databook(sets=[data, more_people])
with open("report.xlsx", "wb") as f:
    f.write(book.export("xlsx"))
```

One dataset, any format. Import from one, export to another. The data doesn't care about file formats, and neither should you.

## The Story

Tablib was one of my first open source projects, built in 2010 before the data science ecosystem in Python really took off. It came from a simple frustration: I kept writing the same import/export boilerplate for every project that dealt with tabular data.

The idea was format agnosticism. Your data is your data. Whether it ends up as a spreadsheet, a JSON file, or a DataFrame shouldn't change how you work with it. That principle — that software should adapt to your workflow rather than the other way around — became central to everything I built after.

Tablib powers the export functionality in [Records](/software/records), and its approach to clean API design directly influenced [Requests](/software/requests). Looking back, it was the first place I figured out what "for humans" actually meant in practice: a single object that does the obvious thing, with sane defaults and no ceremony.

Now maintained by the [Jazzband](https://jazzband.co/) community, which is a model for sustainable open source stewardship.

## Install

```bash
$ uv add tablib
```

For specific format support:

```bash
$ uv add tablib[xlsx]    # Excel support
$ uv add tablib[yaml]    # YAML support
$ uv add tablib[pandas]  # DataFrame support
$ uv add tablib[all]     # Everything
```

## Resources

- [Documentation](https://tablib.readthedocs.io/)
- [Source Code on GitHub](https://github.com/jazzband/tablib)
- [Python Package Index](https://pypi.org/project/tablib/)

## Related

- [**Records**](/software/records) — SQL for Humans, powered by Tablib's export engine.
- [**The Lego Bricks Era**](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed) — The era when these libraries came together.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — How designing for humans became a worldview.
