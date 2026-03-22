# Records: SQL for Humans

Records is a simple library for making raw SQL queries to most relational databases. It's powered by SQLAlchemy, but you'd never know it. No ORM. No models. Just SQL in, results out.

    $ uv pip install records

## What It Looks Like

```python
import records

db = records.Database("postgres://user:pass@localhost/mydb")

# Run a query.
rows = db.query("SELECT * FROM users WHERE active = true")

# Iterate over results.
for row in rows:
    print(row.name, row.email)

# Export to CSV.
print(rows.export("csv"))

# Export to JSON.
print(rows.export("json"))

# Export to Excel.
with open("report.xlsx", "wb") as f:
    f.write(rows.export("xlsx"))

# Export to a pandas DataFrame.
df = rows.export("df")
```

That's it. Connect, query, export. The full [Tablib](/software/tablib) integration means your query results can become CSV, JSON, Excel, YAML, or a DataFrame with a single method call.

## The Philosophy

Sometimes you don't need an ORM. You know SQL. Your database knows SQL. The only thing standing between you and your data is boilerplate. Records removes the boilerplate.

It supports PostgreSQL, MySQL, SQLite, Oracle, MS-SQL, and RedShift. You bring the driver, Records brings the interface. Database URLs work the same way they do in [dj-database-url](/software/dj-database-url) and every twelve-factor app you've ever deployed.

## Install

```bash
$ uv pip install records
```

Database drivers are not included. Install the one you need:

```bash
$ uv pip install psycopg2    # PostgreSQL
$ uv pip install pymysql      # MySQL
```

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/records)
- [Python Package Index](https://pypi.org/project/records/)

## Related

- [**Tablib**](/software/tablib) — The dataset library that powers Records' export functionality.
- [**dj-database-url**](/software/dj-database-url) — Database URLs for Django, born from the same Heroku-era thinking.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — The "for humans" philosophy applied everywhere.
