# ShowMe v1.0.0 Released

  This weekend, I released a new Python module to PyPi: ShowMe v1\.0\.0\.ShowMe is a simple set of function decorators that give you easy diagnose common problems in your Python applications. 

 \#\#\# Basic Usage

  @showme.tracedef complex\_function(a, b, c, \*\*kwargs):....

  \>\>\> complex\_function('alpha', 'beta', False, debug\=True)calling haystack.submodule.complex\_function() withargs: ({'a': 'alpha', 'b': 'beta', 'c': False},)kwargs: {'debug': True}

 It currently supports: 

 \* Argument call tracing\* Execution Time (in seconds)\* CPU Execution Time\* Docstrings

 Roadmap:

 \* Add @showme.locals Support\* Add @showme.globals Support

 Installation

  pip install showme

 \[\[Source on GitHub](http://github.com/kennethreitz/showme)]

  