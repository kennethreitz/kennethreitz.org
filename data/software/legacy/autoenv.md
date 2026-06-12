# Autoenv: Directory-Based Environments

Autoenv activates environments when you `cd` into a directory. Drop a `.env` file in your project, and entering that directory sources it automatically. Leave, and you're back where you started.

It still works, and [Edwin Kofler](https://github.com/hyperupcall) maintains it now. But for new projects you should use [direnv](https://direnv.net/) instead. It does the same job with more care: better performance, an explicit allow-list so a cloned repo can't run arbitrary shell code on you, and `.envrc` unloading when you leave a directory. I recommend it without reservation, and there's no bruised ego in saying so. Autoenv proved people wanted this; direnv built it properly.

## How It Works

Create a `.env` file in your project directory:

```bash
# .env
export API_KEY=blah-blah
export DEBUG=true
```

When you `cd` into the directory, autoenv sources the file.<label for="sn-shell-hook" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-shell-hook" class="margin-toggle"/><span class="sidenote">It works by hooking the shell's `cd` command through your `.bashrc` or `.zshrc`, intercepting directory changes and checking for `.env` files. Elegant and slightly terrifying, which describes a lot of shell tooling.</span> Your environment variables are set, your virtualenv activates, your project context is just *there*. The idea was to make the right environment automatic, because anything manual eventually gets skipped.

## The Idea That Stuck

Autoenv's premise outlived its implementation: your tools should know where they are. Walking into a project directory and having the environment configure itself is now table stakes, built into direnv, IDEs, and every modern dev workflow. The convention of project-level `.env` files became ubiquitous far beyond this little shell script.

That's the pattern with most of [the legacy shelf](/software/legacy). The code gets superseded. The expectation it created doesn't.

## Resources

- [Source Code on GitHub](https://github.com/hyperupcall/autoenv): maintained by Edwin Kofler.
- [direnv](https://direnv.net/): what you should actually use.

## Related

- [**Pipenv**](/software/pipenv): another take on making project environments automatic.
- [**clint**](/software/legacy/clint): a fellow resident of the legacy shelf.
