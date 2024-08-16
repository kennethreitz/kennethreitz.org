# delegator

Delegator is a Python library that allows you to define and execute shell commands in a more readable and maintainable way. It is a wrapper around the `subprocess` module and provides a more high-level interface for running shell commands.

## Key Features

- **Simplified API:** Delegator abstracts away the complexity of the `subprocess` module and provides a more user-friendly API for executing shell commands.
- **Command Chaining:** You can chain multiple commands together using the `|` operator, similar to how you would in a shell script.
- **Output Handling:** Delegator provides methods for capturing and processing the output of shell commands, making it easy to work with the results.
- **Error Handling:** You can easily handle errors and exceptions that occur during command execution, allowing you to build robust shell scripts.
- **Cross-Platform:** Delegator works on all major platforms, including Windows, macOS, and Linux, making it a versatile tool for shell scripting.

## Installation

You can install Delegator using `uv` or `pip`:

```bash
$ uv pip install delegator.py
```

## Usage

Here's a simple example of how you can use Delegator to run a shell command:

```python
import delegator

c = delegator.run('ls -l')
print(c.out)
```

In this example, we use the `run` function to execute the `ls -l` command and print the output to the console.

## Command Chaining

Delegator allows you to chain multiple commands together using the `|` operator. Here's an example:

```python
import delegator

c = delegator.chain('ls -l | grep .py')
print(c.out)
```

In this example, we use the `chain` function to run the `ls -l | grep .py` command, which lists all Python files in the current directory.

## Predecessor — Envoy

`envoy` is a similar library that provides a high-level interface for subprocess management in Python. Delegator is a more modern and feature-rich alternative to Envoy, with additional functionality and improved performance. It has also been battle–tested in production environments and is used by [pipenv](/software/pipenv.md) for shell command execution.
