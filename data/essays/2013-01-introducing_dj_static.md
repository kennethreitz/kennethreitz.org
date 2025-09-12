# Introducing DJ-Static
*January 2013*

![](https://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666514042-8LZBGIPDISPSA4D30E0C/cdc6c-img.jpg)

Django [doesn't recommend](https://docs.djangoproject.com/en/1.5/howto/static-files/#admonition-serving-the-files) the production use of its static file server for a number of reasons. There exists, however, a lovely WSGI application aptly named [Static](http://lukearno.com/projects/static/).

Thus, [DJ-Static](https://github.com/kennethreitz/dj-static) was born.

> Finally, a super-simple way of serving assets in Django that'll actually perform well — [@jacobian](https://twitter.com/jacobian/status/356754168075128833)

## Installation and Configuration

```bash
$ pip install dj-static
```

Configure your static assets in `settings.py`:

```python
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'
```

Then, update your `wsgi.py` file to use DJ-Static:

```python
from django.core.wsgi import get_wsgi_application
from dj_static import Cling

application = Cling(get_wsgi_application())
```

That's it! Django deployment has never been simpler.

## Benefits

Serving static files from Python greatly simplifies the deployment process. The fewer moving parts your application has, the fewer parts there are to break unexpectedly.

Most importantly, this facilitates [Dev/prod parity](http://12factor.net/dev-prod-parity), which should be a goal of all developers.

## What about a CDN?

If you have to ask that question, there's actually quite a good chance you don't. Static responses aren't very different than dynamic ones, especially when using the HTTP Cache headers that DJ-Static provides.

If you're running a top-tier application, optimizing for delivery and reducing frontend load, you will want to explore using a CDN with [Django-Storages](http://django-storages.readthedocs.org/en/latest/).

### Related Links

* [DJ-Static on PyPi](https://pypi.python.org/pypi/dj-static)
* [DJ-Static on GitHub](https://github.com/kennethreitz/dj-static)
* [Django and Static Assets on Heroku](https://devcenter.heroku.com/articles/django-assets)
* [The 12 Factor App: Dev/prod Parity](http://12factor.net/dev-prod-parity)