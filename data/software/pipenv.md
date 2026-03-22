# Pipenv: Python Dev Workflow for Humans

Pipenv brings together `pip` and `virtualenv` into a single tool that manages your project's dependencies the way you actually think about them. No more juggling `requirements.txt` files and manually activating virtual environments.

    $ uv pip install pipenv

## What It Looks Like

```bash
# Start a new project.
$ pipenv install requests

# Pipenv creates a virtual environment, installs the package,
# and generates both Pipfile and Pipfile.lock automatically.

# Add a dev dependency.
$ pipenv install pytest --dev

# Activate the environment.
$ pipenv shell

# Run a command inside the environment.
$ pipenv run python app.py

# Install from an existing Pipfile.
$ pipenv install

# See your dependency graph.
$ pipenv graph
```

Every command does what you'd guess it does. No memorizing activation scripts. No wondering which `requirements.txt` is current.

## The Problem

Before Pipenv, the Python dependency workflow looked like this: create a virtualenv manually, activate it (differently on every OS), pip install things, remember to `pip freeze > requirements.txt`, hope your colleagues have the same versions, discover they don't, debug for an hour. The tools worked. The workflow was hostile.

Pipenv replaced all of that with a single command-line tool. `Pipfile` replaced `requirements.txt` with something readable. `Pipfile.lock` gave Python deterministic builds, the way npm and Ruby's Bundler had for years. Hash verification meant you could trust your dependencies hadn't been tampered with.

The Python Packaging Authority adopted it as a recommended tool. It wasn't a technical breakthrough. It was a workflow breakthrough. The same philosophy behind [Requests](/software/requests): if developers keep making the same mistakes, the tool is wrong, not the developers.

Today, [uv](https://github.com/astral-sh/uv) from Astral is Pipenv's spiritual successor. It solves the same problems faster, with a broader scope, and it's built by a team rather than a single maintainer. That's a good thing. The ideas Pipenv introduced, unified dependency management, lockfiles for Python, developer experience as a first-class concern, live on in better implementations. That's exactly how open source should work.

## Install

```bash
$ uv pip install pipenv
```

## Resources

- [Documentation](https://pipenv.pypa.io/)
- [Source Code on GitHub](https://github.com/pypa/pipenv)
- [Python Package Index](https://pypi.org/project/pipenv/)

## Related

- [**Requests**](/software/requests) — The library whose philosophy Pipenv extends to packaging.
- [**The Lego Bricks Era**](/essays/2026-03-18-values_i_outgrew_and_the_ones_that_stayed) — The era of Python tooling that produced Pipenv.
- [**From HTTP to Consciousness**](/essays/2025-08-27-from_http_to_consciousness) — How "for humans" became a design philosophy.
