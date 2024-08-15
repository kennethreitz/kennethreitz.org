# Introducing Records: SQL for Humans™

    ![](https://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666521244-CB274HKKRV8TKXMXTN79/e44c8-img.jpg)         ![87fe8-img.jpg](http://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666457399-LVQPUG8L3BGBS81NW7AE/2f778-87fe8-img.jpg)      View fullsize ![](http://images.squarespace-cdn.com/content/v1/665498111876725f7613f1e6/1719666472797-RH5Y7RNOZNEH49S6KSW2/2ab21-6d868-image-asset.jpeg)   Records is a very simple, but powerful, library for making raw SQLqueries to Postgres databases.

 This common task can be surprisingly difficult with the standard toolsavailable. This library strives to make this workflow as simple aspossible, while providing an elegant interface to work with your queryresults.

 We know how to write SQL, so let's send some to our database:

 
```
import recordsdb = records.Database('postgres://...')rows = db.query('select * from active_users')
```
 ## ☤ The Basics

 Rows are represented as standard Python dictionaries: `{'column-name': 'value'}`.

 Grab one row at a time:

 
```
>>> rows.next(){'username': 'hansolo', 'name': 'Henry Ford', 'active': True, 'timezone': datetime.datetime(2016, 2, 6, 22, 28, 23, 894202), 'user_email': 'hansolo@gmail.com'}
```
 Or iterate over them:

 
```
for row in rows:spam_user(name=row['name'], email=row['user_email'])
```
 Or store them all for later reference:

 
```
>>> rows.all()[{'username': ...}, {'username': ...}, {'username': ...}, ...]
```
 ## ☤ Features

 * HSTORE support, if available.
* Iterated rows are cached for future reference.
* `$DATABASE_URL` environment variable support.
* Convenience `Database.get_table_names` method.
* Queries can be passed as strings or filenames, parameters supported.
* Safe [parameterization](http://initd.org/psycopg/docs/usage.html): `Database.query('life=%s', params=('42',))`
* Query results are iterators of standard Python dictionaries: `{'column-name': 'value'}`

 Records is proudly powered by [Psycopg2](https://pypi.python.org/pypi/psycopg2)and [Tablib](http://docs.python-tablib.org/en/latest/).

 ## ☤ Data Export Functionality

 Records also features full Tablib integration (my first popular project!), and allows you to exportyour results to CSV, XLS, JSON, or YAML with a single line of code.

 Excellent for sharing data with friends, or generating reports.

 
```
>>> print rows.datasetusername|active|name |user_email |timezone--------|------|----------|-----------------|--------------------------hansolo |True |Henry Ford|hansolo@gmail.com|2016-02-06 22:28:23.894202...
```
 Export your query results to CSV:

 
```
>>> print rows.dataset.csvusername,active,name,user_email,timezonehansolo,True,Henry Ford,hansolo@gmail.com,2016-02-06 22:28:23.894202...
```
 YAML:

 
```
>>> print rows.dataset.yaml- {active: true, name: Henry Ford, timezone: '2016-02-06 22:28:23.894202', user_email: hansolo@gmail.com, username: hansolo}...
```
 JSON:

 
```
>>> print rows.dataset.json[{"username": "hansolo", "active": true, "name": "Henry Ford", "user_email": "hansolo@gmail.com", "timezone": "2016-02-06 22:28:23.894202"}, ...]
```
 Excel:

 
```
with open('report.xls', 'wb') as f:f.write(rows.dataset.xls)
```
 You get the point. Of course, all other features of Tablib are alsoavailable, so you can sort results, add/remove columns/rows, removeduplicates, tranpose the table, add separators, slice data by column,and more.

 See the [Tablib Documentation](http://docs.python-tablib.org/en/latest/)for more details.

 ## ☤ Installation

 Of course, the recommended installation method is pip:

 
```
$ pip install records
```
 ✨🍰✨

 ## ☤ Hyperinks!

 * [Records on GitHub](https://github.com/kennethreitz/records)
* [Records on PyPi](https://pypi.python.org/pypi/records/)
* [Tablib Documentation](http://docs.python-tablib.org/en/latest/)
* [Psycopg2 Documentation](http://initd.org/psycopg/docs/)

  