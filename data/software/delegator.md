# Delegator: Subprocesses for Humans

Delegator is a Python library for running shell commands without fighting `subprocess`. One function call. Real piping. Sane defaults.

    $ uv pip install delegator.py

## What It Looks Like

```python
import delegator

# Run a command.
c = delegator.run("ls -la")
print(c.out)
print(c.return_code)
# 0

# Pipe commands together.
c = delegator.chain("ps aux | grep python")
print(c.out)

# Check for errors.
c = delegator.run("cat nonexistent.txt")
print(c.err)
# cat: nonexistent.txt: No such file or directory

# Run with a timeout.
c = delegator.run("sleep 100", timeout=5)
```

No `subprocess.Popen` arguments to look up. No shell=True debates. No manual pipe wiring. Just run the command and get the result.

## The Philosophy

Python's `subprocess` module is one of the most powerful and most frustrating parts of the standard library. The number of arguments to `Popen` is staggering. The difference between `run`, `call`, `check_output`, and `Popen` trips up experienced developers. Piping two commands together requires more code than the commands themselves.

Delegator started as a rewrite of my earlier library `envoy`. Same idea, better execution. It provides the two things you actually need: run a command, chain commands together. Everything else is handled with sensible defaults.

[Pipenv](/software/pipenv) uses Delegator internally for shell command execution. It's the kind of library that quietly makes other tools possible.

The project was gifted to [Amit Tripathi](https://github.com/amitt001), who now maintains it.

## Install

```bash
$ uv pip install delegator.py
```

## Resources

- [Source Code on GitHub](https://github.com/amitt001/delegator.py)
- [Python Package Index](https://pypi.org/project/delegator.py/)

## Related

- [**Pipenv**](/software/pipenv) — Uses Delegator for shell command execution.
- [**Legit**](/software/legit) — Another tool for making command-line workflows more human.
- [**Requests**](/software/requests) — The "for humans" philosophy that inspired Delegator's design.
