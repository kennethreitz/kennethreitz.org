# ShowMe v1.0.0 Released
*January 2010*

This weekend, I released a new Python module to PyPI: ShowMe v1.0.0.

ShowMe is a simple set of function decorators that give you easy diagnosis of common problems in your Python applications.

## Basic Usage

```python
@showme.trace
def complex_function(a, b, c, **kwargs):
    ...
```

```python
>>> complex_function('alpha', 'beta', False, debug=True)
calling haystack.submodule.complex_function() with
args: ({'a': 'alpha', 'b': 'beta', 'c': False},)
kwargs: {'debug': True}
```


It currently supports:

* Argument call tracing
* Execution Time (in seconds)
* CPU Execution Time
* Docstrings


## Roadmap

* Add `@showme.locals` Support
* Add `@showme.globals` Support


## Installation

```bash
$ pip install showme
```

**Links:**
- [Source on GitHub](http://github.com/kennethreitz/showme)

