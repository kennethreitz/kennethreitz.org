# dj-database-url: Database URLs for Django

A simple Django utility that lets you configure your database with a single environment variable. Born at Heroku, where every twelve-factor app needed this and nothing provided it.

    $ uv pip install dj-database-url

## What It Looks Like

```python
# settings.py
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default="sqlite:///db.sqlite3",
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

That's it. Set `DATABASE_URL` in your environment, and your Django app connects to the right database. Works with PostgreSQL, MySQL, SQLite, Oracle, and more.

```bash
# In development.
export DATABASE_URL=sqlite:///db.sqlite3

# In production.
export DATABASE_URL=postgres://user:pass@host:5432/dbname

# Your code doesn't change. Your settings.py stays the same.
```

## The Story

I built this at Heroku, where we needed Django apps to configure themselves from environment variables. The traditional Django `DATABASES` setting required you to break a connection URL into six separate fields: engine, name, user, password, host, port. Every deployment platform gave you a URL. Django wanted a dictionary. Somebody had to translate.

dj-database-url does that translation. One import, one function call, one environment variable. It became so standard in the Django ecosystem that the pattern spread to other frameworks. The idea that configuration should come from the environment, not from files checked into version control, is now common practice.

## Install

```bash
$ uv pip install dj-database-url
```

## Resources

- [Source Code on GitHub](https://github.com/jazzband/dj-database-url)
- [Python Package Index](https://pypi.org/project/dj-database-url/)

## Related

- [**Records**](/software/records) — SQL for Humans, using the same database URL pattern.
- [**Requests**](/software/requests) — The "for humans" philosophy applied to HTTP.
