---
type: project
category: python-library
status: Active
tags: [library/python-library]
class: Software
---

> *Format-Agnostic Tabular Datasets: The first major success*

---

## Overview

| Attribute | Value |
|-----------|-------|
| **Created** | 2010 |
| **Language** | Python |
| **Philosophy** | Format-agnostic data handling |
| **Status** | Maintained |

---

## Description

Tablib handles tabular data: import from one format, export to another, manipulate in between. It abstracts away format differences so you can focus on the data.

Supports: CSV, JSON, YAML, Excel (xlsx, xls), ODS, HTML, TSV, and more.

---

## The First Success

Tablib was Kenneth's first major open source success, predating [[requests]] by about a year. Early adoption by major companies (Digg, Discovery Channel, Northrop Grumman) established his reputation.

This is also where the NetApp conflict happened, the company tried to claim ownership of tablib and other personal projects. Kenneth refused and left. That moment of choosing code ownership over employment shaped everything that followed.

---

## Usage

```python
import tablib

# Create a dataset
data = tablib.Dataset()
data.headers = ['Name', 'Age', 'City']
data.append(['Ada', 36, 'Paris'])
data.append(['Grace', 33, 'Paris'])

# Export to any format
data.export('csv')
data.export('json')
data.export('xlsx')

# Import from any format
data = tablib.Dataset().load(open('data.csv').read())
```

---

## Design Philosophy

Same principles that would define [[requests]]: simple API for common operations, format details hidden from user, just works out of the box, progressive disclosure of complexity.

---

## Supported Formats

| Format | Import | Export | Notes |
|--------|--------|--------|-------|
| CSV | Yes | Yes | The universal exchange format |
| JSON | Yes | Yes | Nested structure preserved |
| YAML | Yes | Yes | Human-readable serialization |
| Excel (xlsx) | Yes | Yes | Via openpyxl |
| Excel (xls) | Yes | Yes | Legacy format |
| ODS | Yes | Yes | LibreOffice native |
| HTML | No | Yes | Table rendering |
| TSV | Yes | Yes | Tab-separated |
| LaTeX | No | Yes | Academic publishing |

The power is in the interoperability: load from any format, manipulate in Python, export to any other format. One API regardless of source or destination.

---

## Legacy

Tablib proved that Kenneth's design sensibility worked. It validated the approach before [[requests]] made it famous. It also powers [[records]]' export functionality, the libraries compose together, simple tools building on simple tools.

---

## Related

- [[requests]]: The breakthrough that followed
- [[records]]: Uses tablib for exports
- [[Python Libraries]]: Full ecosystem
- [[Career Timeline]]: The NetApp story
- [[For Humans]]: The philosophy
- [[Tablib Dataset Library v0.6.1 Released!]]: Early release announcement

---

*The first proof that "For Humans" works.*

partOf:: [[Library/Python Libraries/Python Libraries|Python Libraries]]
