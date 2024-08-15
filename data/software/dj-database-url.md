# dj-database-url

`dj-database-url` is a Python library that allows you to configure your Django application to use a database URL.

This need arose at my time at Heroku, where we allowed users to configure their Django application by setting an environment variable called `DATABASE_URL`.

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


There are many options you can pass to `dj-database-url.config()`. See the [dj-database-url documentation](https://pypi.org/project/dj-database-url/) for more information.

https://pypi.org/project/dj-database-url/
