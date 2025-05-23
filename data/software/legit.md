# legit

Legit is a simple command line tool that helps to manage your project repositories. It takes care of creating, deleting, and switching between branches. A Python script that wraps Git, it is designed to be used as a standalone tool, but it can also be used via Git aliases.


It is inspired by [GitHub for Mac](https://docs.github.com/en/desktop/installing-and-authenticating-to-github-desktop/installing-github-desktop), which is a great tool for managing Git repositories. Legit aims to bring the same level of ease to the command line.

This is a fairly old project, created in 2011. I've been using it for a while now and it has saved me a lot of time.

## Installation

To install legit, you can use the following command:

```bash
$ uv pip install legit
```

If you're on a Mac, you can also use Homebrew:

```bash
$ brew install legit
```

## Usage

First, you have to install the git aliases:

```bash
$ legit --install
```

Syncronizes the given branch. Defaults to current branch. Stash, Fetch, Auto\-Merge/Rebase, Push, and Unstash:

```bash
$ git sync
```

Publish a specified branch to the remote.

```bash
$ git publish
```

Removes specified branch from the remote.

```bash
$ git unpublish
```

Undos the last commit.

```bash
$ git undo
```

Get a nice pretty list of available branches.

```bash
$ git branches
```

**Note**: All of the above commands are aliases for `legit` commands.

## Further Notes

Many thanks to [Frost Ming](https://github.com/frostming) for maintaining this project.

- https://github.com/frostming/legit
- https://pypi.org/project/legit/

Enjoy!
