# Records: SQL for Humans

Records is a simple library for making raw SQL queries to most relational databases. It's powered by SQLAlchemy, but you'd never know it. No ORM. No models. Just SQL in, results out.

    $ uv add records

## What It Looks Like

```python
import records

db = records.Database("postgres://user:pass@localhost/mydb")

# Run a query.
rows = db.query("SELECT * FROM users WHERE active = true")

# Iterate over results.
for row in rows:
    print(row.name, row.email)

# Access columns by name or index.
first = rows[0]
print(first.name)
print(first["email"])

# Parameterized queries. Always use these.
rows = db.query(
    "SELECT * FROM users WHERE city = :city AND age > :age",
    city="Portland",
    age=25,
)

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

Connect, query, export. The full [Tablib](/software/tablib) integration means your query results can become CSV, JSON, Excel, YAML, or a DataFrame with a single method call.

## The Philosophy

Sometimes you don't need an ORM. You know SQL. Your database knows SQL. The only thing standing between you and your data is boilerplate. Records removes the boilerplate.

It supports PostgreSQL, MySQL, SQLite, Oracle, MS-SQL, and Redshift. You bring the driver, Records brings the interface. Database URLs work the same way they do in [dj-database-url](/software/dj-database-url) and every twelve-factor app you've ever deployed.

## The Story

Records came from my time at Heroku, where talking to databases was something every application did and every developer did slightly differently. I wanted a library where the code looked like what you were doing: connect to a database, run a query, get the results. Three lines for three actions.

The export integration with [Tablib](/software/tablib) was the part that surprised me. Once your query results can become any tabular format with a single method call, a lot of "reporting" and "data pipeline" tasks collapse into a few lines of Python. That accidental synergy between two libraries I'd written years apart taught me something about how good abstractions compose.

Records is proof that not everything needs to be an ORM. Sometimes the most powerful interface is the one that gets out of the way and lets you write the SQL you were going to write anyway.

## Install

```bash
$ uv add records
```

Database drivers are not included. Install the one you need:

```bash
$ uv add psycopg2    # PostgreSQL
$ uv add pymysql      # MySQL
```

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/records)
- [Python Package Index](https://pypi.org/project/records/)

<!-- vault:history start -->
## History

Records provides a simple way to run SQL queries and get results back as nice objects. No ORM, no complex setup, just SQL in, data out.

Built on SQLAlchemy but hides the complexity. You write SQL; records handles the rest.

ORMs are powerful but heavy. Sometimes you just want to:
1. Connect to a database
2. Run a query
3. Get results

Why should that require learning an entire abstraction layer?

SQL is fine: don't hide it, embrace it. Simple connection (one string, one object), nice results (attribute access, not dictionary fumbling), and export anywhere through integration with [tablib](/software/tablib) for format handling.

ORMs solve real problems, but they also create new ones. They add a translation layer between your intention and the database. They generate SQL you didn't write and can't always predict. They require learning an abstraction that sits between you and the thing you actually want to do. For simple queries, they're overhead. For complex queries, they're a prison.

Records takes the opposite stance: SQL is already a good language for talking to databases. The problem was never SQL, it was Python's interface to it. So records fixes the interface and leaves the language alone.

Records uses [tablib](/software/tablib) under the hood for exports, the libraries work together. Query a database, get results, export to CSV or Excel or JSON with one call. This is the "For Humans" ecosystem in action: simple tools that compose. The same data flows from database through records into tablib into whatever format you need.
<!-- vault:history end -->

## Related

- [**Tablib**](/software/tablib): The dataset library that powers Records' export functionality.
- [**dj-database-url**](/software/dj-database-url): Database URLs for Django, born from the same Heroku-era thinking.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness): The "for humans" philosophy applied everywhere.
- [**The Lego Bricks Era**](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed): The golden era that produced these libraries.
