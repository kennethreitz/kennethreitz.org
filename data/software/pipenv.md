# Pipenv

[Pipenv](https://pipenv.pypa.io/) is a tool for managing Python dependencies. It is a wrapper around pip and virtualenv.

https://github.com/pypa/pipenv


## Why Use Pipenv?

- **Unified Workflow:** Pipenv streamlines the process of managing your project's dependencies and virtual environments into a single command-line tool, making it easier to keep everything organized.

- **Automatic Virtual Environments:** When you install a package, Pipenv automatically creates a virtual environment and installs your packages within it, keeping your global Python environment clean.

- **Lockfiles for Deterministic Builds:** Pipenv uses a `Pipfile` to specify your dependencies and a `Pipfile.lock` to lock them down. This ensures that you and your team always install the exact same versions, minimizing the "works on my machine" problem.

- **Enhanced Security:** By leveraging hash verification, Pipenv ensures that the packages you install are secure and haven't been tampered with.

- **Simplified Dependency Management:** Pipenv abstracts away the complexity of managing dependencies, making it easier for developers to focus on writing code instead of wrestling with dependency issues.

## Key Features

- **Pipfile and Pipfile.lock:** These files replace the traditional `requirements.txt`, offering a more readable and secure way to manage dependencies.
- **Automatic environment management:** Automatically create and manage a virtual environment for your project.
- **Seamless integration:** Works perfectly with Python's `pip` and `virtualenv`, making it an easy transition for users familiar with these tools.
- **Cross-platform support:** Pipenv works across all major platforms, ensuring a consistent experience for all developers.

## Get Started with Pipenv

To get started with Pipenv, simply install it using `pip`:

```bash
$ pip install pipenv
```

After installation, you can create a new project, install dependencies, and start working in an isolated environment:

```bash
$ pipenv install requests
$ pipenv shell
```

Pipenv will handle the rest, from setting up the environment to locking your dependencies. Whether you are a seasoned Python developer or just getting started, Pipenv simplifies your workflow, allowing you to focus on what truly matters—building great software.
