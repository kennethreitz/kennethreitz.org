# Introducing DJ-Static

 ![](https://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666514042-8LZBGIPDISPSA4D30E0C/cdc6c-img.jpg)      ![499f4-img.jpg](http://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666449350-0PEMOLE2R6AHK7SNZ26O/4bfef-499f4-img.jpg)    ![687474703a2f2f6661726d382e737461746963666c69636b722e636f6d2f373338372f383930373335313939305f353836373764376333355f7a2e6a7067](http://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666476621-0F1OGIEN3TRR2P7H82XU/3def4-e54d6-687474703a2f2f6661726d382e737461746963666c69636b722e636f6d2f373338372f383930373335313939305f353836373764376333355f7a2e6a7067.jpeg)   Django [doesn't recommend](https://docs.djangoproject.com/en/1.5/howto/static-files/#admonition-serving-the-files) the production use of its static file server for a number of reasons. There exists, however, a lovely WSGI application aptly named [Static](http://lukearno.com/projects/static/).

 Thus, [DJ\-Static](https://github.com/kennethreitz/dj-static) was born.


> Finally, a super\-simple way of serving assets in Django that’ll actually perform well — [@jacobian](https://twitter.com/jacobian/status/356754168075128833)

 ## Installation and Configuration

 $ pip install dj\-static

 Configure your static assets in `settings.py`:


```
STATIC_ROOT = 'staticfiles'STATIC_URL = '/static/'
```
 Then, update your `wsgi.py` file to use DJ\-Static:


```
from django.core.wsgiimport get_wsgi_applicationfrom dj_static import Clingapplication = Cling(get_wsgi_application())
```
 That's it! Django deployment has never been simpler.

 ## Benefits

 Serving static files from Python greatly simplifies the deployment process. The fewer moving parts your application has, the fewer parts there are to break unexpectedly.

 Most importantly, this facilitates [Dev/prod parity](http://12factor.net/dev-prod-parity), which should be a goal of all developers.

 ## What about a CDN?

 If you have to ask that question, there's actually quite a good chance you don't. Static responses aren't very different than dynamic ones, especially when using the HTTP Cache headers that DJ\-Static provides.

 If you're running a top\-tier application, optimizing for delivery and reducing frontend load, you will want to explore using a CDN with [Django\-Storages](http://django-storages.readthedocs.org/en/latest/).

 ### Related Links

 * [DJ\-Static on PyPi](https://pypi.python.org/pypi/dj-static) \- [DJ\-Static on GitHub](https://github.com/kennethreitz/dj-static) \- [Django and Static Assets on Heroku](https://devcenter.heroku.com/articles/django-assets) \- [The 12 Factor App: Dev/prod Parity](http://12factor.net/dev-prod-parity)
