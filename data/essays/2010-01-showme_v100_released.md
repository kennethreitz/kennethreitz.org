# ShowMe v1.0.0 Released
*January 2010*





<label for="sn-dev-philosophy" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-dev-philosophy" class="margin-toggle"/><span class="sidenote">This announcement reflects the era of rapid Python library development, where individual developers could create and distribute debugging tools with minimal friction. The focus on "easy diagnosis" anticipates modern observability practices.</span>

  This weekend, I released a new Python module to PyPi: ShowMe v1\.0\.0\.ShowMe is a simple set of function decorators that give you easy diagnose common problems in your Python applications. 

 \#\#\# Basic Usage

  @showme.tracedef complex\_function(a, b, c, \*\*kwargs):....

  \>\>\> complex\_function('alpha', 'beta', False, debug\=True)calling haystack.submodule.complex\_function() withargs: ({'a': 'alpha', 'b': 'beta', 'c': False},)kwargs: {'debug': True}<label for="sn-decorator-pattern" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-decorator-pattern" class="margin-toggle"/><span class="sidenote">The use of decorators for tracing demonstrates early adoption of Pythonic debugging patterns. This approach would later influence modern APM tools and logging frameworks that use similar non-invasive instrumentation.</span>

 It currently supports: 

 \* Argument call tracing\* Execution Time (in seconds)\* CPU Execution Time\* Docstrings<label for="sn-observability" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-observability" class="margin-toggle"/><span class="sidenote">These four capabilities represent core observability primitives that would become standard in production Python applications. The inclusion of docstring support suggests an early focus on self-documenting code.</span>

 Roadmap:

 \* Add @showme.locals Support\* Add @showme.globals Support<label for="sn-scope-introspection" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-scope-introspection" class="margin-toggle"/><span class="sidenote">The planned features for locals/globals inspection represent advanced debugging capabilities that would later be incorporated into IDEs and debugging tools like pdb and modern Python debuggers.</span>

 Installation

  pip install showme

 \[\[Source on GitHub](http://github.com/kennethreitz/showme)]<label for="sn-distribution" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-distribution" class="margin-toggle"/><span class="sidenote">The straightforward pip installation and GitHub hosting represent the democratization of Python package distribution that made the language's ecosystem so vibrant. This was cutting-edge developer experience in 2010.</span>

  