# Clint: An Early CLI Toolkit

Clint was one of my first open source projects, a toolkit for building command-line applications in Python.<label for="sn-early-cli" class="margin-toggle sidenote-number"></label><input type="checkbox" id="sn-early-cli" class="margin-toggle"/><span class="sidenote">Clint arrived in the early 2010s, when Python CLI tooling was far less mature. Click came in 2014, Typer in 2019, Rich in 2020. The ecosystem Clint was built for no longer exists, which is the happiest fate a stopgap tool can have.</span> It's unmaintained now, and you shouldn't use it. I keep this page because the project taught me things I still use, and because pretending old work doesn't exist is its own kind of dishonesty.

## What It Did

Clint collected the small things every command-line tool needs and made them pleasant:

- **Colored output**: green for success, red for failure, without ANSI escape codes scattered through your strings.
- **Progress bars**: a one-line loop wrapper, years before this was standard.
- **Column printing**: aligned tabular output for terminals.
- **Interactive prompts**: ask the user a question, get an answer, move on.
- **Argument handling**: a simple layer over raw `sys.argv`.

Nothing in that list is impressive today. All of it was friction in 2011, and removing common friction is most of what I've ever done.

## What Replaced It

Use these instead:

- [**Click**](https://click.palletsprojects.com/): the framework that got Python CLIs right. Decorator-based, composable, battle-tested.
- [**Typer**](https://typer.tiangolo.com/): Click with type hints doing the work.
- [**Rich**](https://rich.readthedocs.io/): beautiful terminal output, progress bars, tables. Everything `clint.textui` wanted to be.
- **argparse**: in the standard library, and better than its reputation.

## What It Taught Me

Clint is where I learned that the standard library being *capable* of something is not the same as it being *humane* about it. You could always color terminal output in Python. You could always parse arguments. The question was how much of your attention it cost, and attention is the scarcest resource a programmer has.

A year later I applied the same observation to `urllib2`, and that one became [Requests](/software/requests). Clint was the rehearsal.

## Resources

- [Source Code on GitHub](https://github.com/kennethreitz/clint): archived, for the curious.

## Related

- [**Legit**](/software/legit): command-line ergonomics applied to Git.
- [**Requests**](/software/requests): the same lesson, applied to HTTP, a year later.
