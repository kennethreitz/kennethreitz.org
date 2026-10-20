# The Hitchhiker's Guide to Python

[python-guide.org](https://python-guide.org/) is an opinionated guide to Python best practices: installation, project structure, code style, testing, deployment, and everything in between. It became one of the most widely referenced Python resources in the world, and eventually an O'Reilly book.

## Why I Built It

When I was learning Python, the advice was scattered across dozens of blog posts, Stack Overflow answers, and mailing list threads, much of it conflicting, some of it outdated. There was no single place that said: "Here's how to set up a Python project properly. Here's how to write clean code. Here's how to ship it."

So I wrote one.

The guide is deliberately opinionated. It doesn't present five options and leave you paralyzed. It says: "Do this. Here's why."<label for="sn-guide-constraints" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-guide-constraints" class="margin-toggle"/><span class="sidenote">Fewer choices, better outcomes: [Constraints as Liberation](/knowledge/key-concepts/constraints-as-liberation).</span> That's what beginners need, and honestly, it's what experienced developers appreciate too. Decision fatigue is the enemy of getting things done.

## What It Covers

- **Getting Started**: Installing Python properly on every platform.
- **Development Environments**: Virtual environments, package management, editor setup.
- **Writing Great Code**: Style, structure, conventions, and the patterns that make Python Python.<label for="sn-guide-python" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-guide-python" class="margin-toggle"/><span class="sidenote">More on the language itself in [Python](/knowledge/technology/python).</span>
- **Shipping Code**: Packaging, distribution, documentation, testing, logging, deployment.
- **Scenario Guides**: Web applications, CLI tools, scientific computing, data analysis, networking.

## The O'Reilly Book

The website grew into *The Hitchhiker's Guide to Python*, published by O'Reilly Media. Taking a community web resource and turning it into a professionally published book was a meaningful milestone. It validated the idea that opinionated, accessible technical writing has real value.

- [Buy on Amazon](https://amzn.to/3SMIm3T)
- [Read Online for Free](https://python-guide.org/)

## Philosophy

The guide embodies the same principle as everything else I build: **if developers are confused, the documentation has failed, not the developer.** Technical writing should meet people where they are, not where the author wishes they were.<label for="sn-guide-for-humans" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-guide-for-humans" class="margin-toggle"/><span class="sidenote">The same idea, generalized: [For Humans](/knowledge/philosophy/for-humans). See also [Design for the Worst Day](/knowledge/philosophy/design-for-the-worst-day).</span>

Python's community has always valued readability and simplicity. The Hitchhiker's Guide tries to live up to that standard not just in the code it recommends, but in the prose that recommends it.

## Example

The guide's advice is concrete. Here's how it walks you through giving a project its own isolated environment, so its dependencies never collide with anything else on your machine:

```bash
$ cd project_folder
$ virtualenv venv
$ source venv/bin/activate
(venv) $ pip install requests
```

And the guide's suggested layout for a small project:

```text
README.rst
LICENSE
setup.py
requirements.txt
sample/__init__.py
sample/core.py
sample/helpers.py
docs/conf.py
docs/index.rst
tests/test_basic.py
tests/test_advanced.py
```

Opinionated, boring, and easy to recognize. That's a feature.

## Today

The guide lives at [docs.python-guide.org](https://docs.python-guide.org/) (python-guide.org redirects there), served as a static site from Netlify. The source is on GitHub at [realpython/python-guide](https://github.com/realpython/python-guide), where it's still being updated, and it's still free to read online.

## Related

- [**pep8.org**](/software/websites/pep8-org): A cleaner presentation of Python's style guide.
- [**Requests**](/software/requests): The "for humans" philosophy applied to code.
- [**Programming as Spiritual Practice**](/essays/2025-08-26-programming_as_spiritual_practice): How writing code consciously changes everything.
