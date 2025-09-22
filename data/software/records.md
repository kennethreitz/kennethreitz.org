# Records: SQL for Humans

Records is a library for working with tabular data in Python, accessible via SQL. It is powered by [SQLAlchemy](https://www.sqlalchemy.org/) and provides a high-level API for interacting with databases using SQL queries. Records simplifies the process of working with databases by abstracting away the complexities of SQL and providing a more user-friendly interface.

<span class="sidenote">Records represents Kenneth's approach to making database interactions more intuitive. While SQLAlchemy provides comprehensive ORM capabilities, Records focuses on the common use case of executing SQL queries and working with results in a Pythonic way.</span>

## Installation

```bash
$ uv pip install records
```

Database support includes RedShift, Postgres, MySQL, SQLite, Oracle, and MS-SQL (drivers not included).

<span class="sidenote">Records supports a wide range of database systems, reflecting the diverse landscape of enterprise data storage. By building on SQLAlchemy's database abstraction layer, Records inherits compatibility with virtually any SQL database.</span>

Records offers full [tablib](/software/tablib) integration, allowing you to easily convert query results to tabular data formats like CSV, JSON, and Excel — and even dataframes.

## Usage

Using `records` is simple, if you have a database connection string like `DATABASE_URL` set in your environment, you can use it like this:

```python
import records

db = records.Database('postgres://...')
rows = db.query('select * from active_users')

# Iterate over rows
for row in rows:
    print(row.username)

# Convert query results to CSV
csv = rows.export('csv')

# Convert query results to JSON
json = rows.export('json')

# Convert query results to Excel
excel = rows.export('xlsx')

# Convert query results to a pandas DataFrame
df = rows.export('df')

<span class="sidenote">The seamless export to pandas DataFrames bridges the gap between SQL databases and the Python data science ecosystem, enabling analysts to move fluidly between database querying and statistical analysis.</span>
```

Make sure you have the appropriate database driver installed.

## Links

- https://github.com/kennethreitz/records
