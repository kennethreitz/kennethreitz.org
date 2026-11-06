# dj-database-url: Database URLs for Django

A simple Django utility that lets you configure your database with a single environment variable. Born at Heroku, where every twelve-factor app needed this and nothing provided it.

    $ uv add dj-database-url

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

## Supported Databases

```python
# PostgreSQL.
DATABASES["default"] = dj_database_url.parse(
    "postgres://user:pass@host:5432/dbname"
)

# MySQL.
DATABASES["default"] = dj_database_url.parse(
    "mysql://user:pass@host:3306/dbname"
)

# SQLite.
DATABASES["default"] = dj_database_url.parse(
    "sqlite:///path/to/db.sqlite3"
)

# PostGIS for geographic data.
DATABASES["default"] = dj_database_url.parse(
    "postgis://user:pass@host:5432/geodata"
)

# You can also parse a URL directly without environment variables.
DATABASES["default"] = dj_database_url.parse(
    os.environ.get("DATABASE_URL", "sqlite:///db.sqlite3"),
    conn_max_age=600,
)
```

Every URL format maps to the correct Django database backend automatically. No looking up engine strings. No remembering which backend class goes with which database.

## The Story

I built this at Heroku, where we needed Django apps to configure themselves from environment variables. The traditional Django `DATABASES` setting required you to break a connection URL into six separate fields: engine, name, user, password, host, port. Every deployment platform gave you a URL. Django wanted a dictionary. Somebody had to translate.

dj-database-url does that translation. One import, one function call, one environment variable. It became so standard in the Django ecosystem that the pattern spread to other frameworks. The idea that configuration should come from the environment, not from files checked into version control, is now common practice. The [twelve-factor app](https://12factor.net/) methodology that inspired it has become conventional wisdom.

This is maybe the smallest library I've written that had the biggest impact on how people deploy Django. It's twelve lines of meaningful code that changed a workflow for thousands of developers. Sometimes that's all it takes: noticing a friction point and removing it.

Now maintained by the [Jazzband](https://jazzband.co/) community.

## Install

```bash
$ uv add dj-database-url
```

## Resources

- [Source Code on GitHub](https://github.com/jazzband/dj-database-url)
- [Python Package Index](https://pypi.org/project/dj-database-url/)

<!-- vault:history start -->
## History

dj-database-url parses database connection URLs (like `postgres://user:pass@host:port/db`) into Django's database configuration dictionary. Essential for 12-Factor app deployment.

Django wants database configuration as a dictionary:

But deployment platforms (Heroku, etc.) provide a single URL:

One line. Works everywhere. Follows 12-Factor principles.

This library emerged from Kenneth's work at Heroku. Heroku provides DATABASE_URL automatically, Django apps need to consume it, and the translation was tedious and error-prone. dj-database-url made it trivial. Infrastructure glue, not glamorous but essential for Django deployment.

The [12-Factor App](https://12factor.net/) methodology (which Heroku championed) recommends storing config in environment variables. dj-database-url makes Django follow this pattern naturally.

Created during Kenneth's "Python Overlord" period at [Heroku](/essays/2011-01-joining_heroku). He was literally building the tools needed to deploy Python apps on the platform. dj-database-url solved a real problem he encountered daily, and then solved it for every Django developer deploying to any platform that provides DATABASE_URL.

The library outlasted his tenure at Heroku. Still downloaded hundreds of thousands of times monthly. Infrastructure glue that quietly holds the Django deployment ecosystem together.
<!-- vault:history end -->

## Related

- [**Records**](/software/records): SQL for Humans, using the same database URL pattern.
- [**Requests**](/software/requests): The "for humans" philosophy applied to HTTP.
- [**The Lego Bricks Era**](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed): The Heroku era that produced these tools.
