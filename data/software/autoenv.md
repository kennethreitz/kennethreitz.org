# autoenv

You can install `autoenv` using `pip` or `uv`, but you should likely use `direnv` instead. It's a superior project, these days.

```bash
$ uv pip install autoenv
```

## Usage

Autoenv allows you to automatically activate a virtual environment when you `cd` into a directory containing a `.env` file. This can be useful for managing project-specific environment variables and dependencies.

To use autoenv, create a `.env` file in your project directory with the necessary environment variables. For example:

```bash
# .env
export API=blah-blah
export SECRET_KEY=super-secret
```

When you `cd` into the project directory, autoenv will automatically activate the environment and set the environment variables defined in the `.env` file. The project accomplishes this by hooking into the shell's `cd` command and sourcing the `.env` file when you enter the directory.

## Conclusion & Alternatives

Autoenv was a popular project for managing project-specific environments, but it is no longer actively maintained. A better alternative is `direnv`, which provides similar functionality with more features and better performance. It is recommended to use `direnv` instead of `autoenv` for managing project environments.

The respository for `autoenv` is available on GitHub, and is actively maintained by [Edwin Kofler](https://github.com/hyperupcall).

- https://github.com/hyperupcall/autoenv
- https://direnv.net/docs/hook.html
