# Tablib Dataset Library v0.6.1 Released!

  I'm pleased to announce a new Python module: \[Tablib](http://github.com/kennethreitz/tablib). Tablib is a simple module for working with tabular datasets. It allows you create tables of data using standard Python datatypes, manipulate them, and easily export to Excel, JSON, YAML, and CSV.\*\*Basic Usage\*\*:

  import tablib

  headers \= ('first\_name', 'last\_name', 'gpa')data \= \[('John', 'Adams', 90\), ('George', 'Washington', 67\)]

  data \= tablib.Dataset(\*data, headers\=headers)

 You can maniuplate your data like a standard Python list:

  \>\>\> data.append(('Henry', 'Ford', 83\))

  \>\>\> print data\['first\_name']\['John', 'George', 'Henry']

  \>\>\> del data\[1]

 You can easily export your data to JSON, YAML, XLS, and CSV.

  \>\>\> print data.json\[{"first\_name": "John", "last\_name": "Adams", "gpa": 90},{"first\_name": "Henry", "last\_name": "Ford", "gpa": 83}]

  \>\>\> print data.yaml\- {age: 90, first\_name: John, last\_name: Adams}\- {age: 83, first\_name: Henry, last\_name: Ford}

  \>\>\> print data.csvfirst\_name,last\_name,ageJohn,Adams,90Henry,Ford,83 

  \>\>\> open('people.xls', 'w').write(data.xls)

 Excel files with multiple sheets are also supported (via the \`DataBook\` object).

 \[\[Source on GitHub](http://github.com/kennethreitz/tablib)] \[\[PyPi Listing](http://pypi.python.org/pypi/tablib)]

  