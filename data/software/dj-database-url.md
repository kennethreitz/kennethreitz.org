# dj-database-url

`dj-database-url` is a Python library that allows you to configure your Django application to use a database URL.

This need arose at my time at Heroku, where we allowed users to configure their Django application by setting an environment variable called `DATABASE_URL`.

<span class="sidenote">This library emerged from Kenneth's work at Heroku, where the twelve-factor app methodology emphasized configuration through environment variables. The simple act of parsing database URLs became essential for cloud-native Django applications.</span>

## The Problem It Solved

<span class="sidenote">Before dj-database-url, Django developers had to manually parse DATABASE_URL strings or maintain separate configuration files for different environments. This was particularly painful when deploying to platforms like Heroku that provided database connections as URLs.</span>

The traditional Django `DATABASES` setting required explicit configuration of database parameters like host, port, user, password, and database name. This worked fine for development, but became cumbersome when deploying to cloud platforms that provided database connection information as a single URL string.

## Installation

Installing `dj-database-url` is simple:

    $ pip install dj-database-url

## Usage

Then, in your `settings.py` file, you can use `dj-database-url` to configure your database:


    import dj_database_url

    DATABASES['default'] = dj_database_url.config(
        conn_max_age=600,
        conn_health_checks=True,
    )

<span class="sidenote">The `conn_max_age` parameter enables connection pooling by keeping database connections alive for the specified number of seconds, reducing the overhead of creating new connections for each request. The `conn_health_checks` parameter ensures connections are tested before use, preventing errors from stale connections.</span>


There are many options you can pass to `dj-database-url.config()`. See the [dj-database-url documentation](https://pypi.org/project/dj-database-url/) for more information.

<span class="sidenote">This library became so essential to Django's ecosystem that similar utilities were created for other frameworks. The pattern of using URL strings for database configuration is now standard across many web frameworks and deployment platforms.</span>

https://pypi.org/project/dj-database-url/
