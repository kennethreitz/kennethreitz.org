# autoenv

You can install `autoenv` using `pip` or `uv`, but you should likely use `direnv` instead<label for="sn-direnv-superior" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-direnv-superior" class="margin-toggle"/><span class="sidenote">Direnv, written in Go, offers better performance and more robust shell integration than the original bash-based autoenv. It also handles more complex scenarios like nested directories and provides better error handling.</span>. It's a superior project, these days.

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

When you `cd` into the project directory, autoenv will automatically activate the environment and set the environment variables defined in the `.env` file. The project accomplishes this by hooking into the shell's `cd` command<label for="sn-shell-hook" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-shell-hook" class="margin-toggle"/><span class="sidenote">This approach requires modifying shell initialization files like `.bashrc` or `.zshrc` to add the autoenv hook, which intercepts directory changes and checks for `.env` files.</span> and sourcing the `.env` file when you enter the directory.

## Conclusion & Alternatives

Autoenv was a popular project for managing project-specific environments, but it is no longer actively maintained. A better alternative is `direnv`, which provides similar functionality with more features and better performance. It is recommended to use `direnv` instead of `autoenv` for managing project environments.

The respository for `autoenv` is available on GitHub, and is actively maintained by [Edwin Kofler](https://github.com/hyperupcall)<label for="sn-maintenance-transfer" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-maintenance-transfer" class="margin-toggle"/><span class="sidenote">Edwin Kofler took over maintenance of the project from Kenneth, ensuring continued support for existing users while the community gradually migrates to more modern alternatives like direnv.</span>.

- https://github.com/hyperupcall/autoenv
- https://direnv.net/docs/hook.html
