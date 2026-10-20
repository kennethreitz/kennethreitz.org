# pep8.org: PEP 8, the Easy Way

[pep8.org](https://pep8.org/) is a cleaner, more readable version of PEP 8, Python's official style guide.

## Why It Exists

PEP 8 is the foundational style guide for Python code. Every Python developer reads it eventually. But the official version on python.org was dense, hard to scan, and not particularly pleasant to read. So I made a nicer version.

The idea was simple: take the same content, apply better typography and formatting, and host it at a memorable URL. No additions, no opinions layered on top. Just PEP 8, presented the way it deserves to be presented.<label for="sn-pep8-design" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-pep8-design" class="margin-toggle"/><span class="sidenote">Typography is part of the interface. See [Design](/knowledge/technology/design).</span>

- Beautiful is better than ugly.
- Explicit is better than implicit.
- Simple is better than complex.
- Complex is better than complicated.

The Zen of Python applies to presenting Python's own style guide, too.

## Impact

pep8.org became a common reference link in code reviews, tutorials, and onboarding documentation. When you want to point a teammate at "use PEP 8 style," a clean, readable URL is better than a link to a PEP index page.<label for="sn-pep8-naming" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-pep8-naming" class="margin-toggle"/><span class="sidenote">A memorable URL is just [naming things](/knowledge/key-concepts/naming-things) well.</span>

It's a small project, barely any code, but it solved a real friction point in how the Python community shares its most important conventions.

## The Broader Pattern

This is a recurring theme in my work: noticing where developers experience unnecessary friction and removing it. The same instinct that produced [Requests](/software/requests) (HTTP shouldn't be hard) and [The Hitchhiker's Guide to Python](/software/websites/python-guide) (best practices shouldn't be scattered) produced pep8.org. Good developer experience is about removing barriers between people and the things they're trying to do.

## Example

The kind of thing PEP 8 asks for, and pep8.org makes easy to find and link to:

```python
# No:
def long_function_name(var_one, var_two,
    var_three, var_four):
    print(var_one)

# Yes:
def long_function_name(
        var_one, var_two, var_three,
        var_four):
    print(var_one)
```

Four spaces per indentation level. Lines limited to 79 characters. `snake_case` for functions, `CapWords` for classes. Small [constraints](/knowledge/key-concepts/constraints-as-liberation) that free a whole community from arguing about formatting.

## Today

pep8.org is still live, served as a static site from Netlify. The [source is on GitHub](https://github.com/kennethreitz/pep8.org), and it hasn't needed much attention in years. That's the point of a static page of good typography: it just keeps working. The canonical text is always [PEP 8 on python.org](https://peps.python.org/pep-0008/).

## Visit

- [pep8.org](https://pep8.org/)
- [Source Code on GitHub](https://github.com/kennethreitz/pep8.org)
- [PEP 8 on python.org](https://peps.python.org/pep-0008/): The canonical text.

## Related

- [**The Hitchhiker's Guide to Python**](/software/websites/python-guide): Another effort to make Python knowledge more accessible.
- [**Requests**](/software/requests): The "for humans" philosophy applied to HTTP.
