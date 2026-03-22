# Legit: Git for Humans

Legit is a command-line tool that adds a layer of sanity to everyday Git workflows. It wraps the most common branch operations into simple, memorable commands.

    $ uv pip install legit

## What It Looks Like

```bash
# Install the Git aliases.
$ legit --install

# Sync your current branch: stash, fetch, merge/rebase, push, unstash.
$ git sync

# Publish a branch to the remote.
$ git publish

# Unpublish a branch from the remote.
$ git unpublish

# Undo the last commit (keeps your changes).
$ git undo

# See all branches, nicely formatted.
$ git branches
#   main         (published)
#   feature-x    (unpublished)
#   fix-login    (published)
```

Each command does one thing and does it safely. `git sync` handles the entire stash-fetch-merge-push cycle that normally takes four separate commands and a good memory.

## The Philosophy

I built Legit in 2011 because I loved the Git workflow in GitHub for Mac and wanted that same clarity on the command line. Git is powerful, but most developers use the same five workflows over and over. Legit packages those workflows into commands that say what they do.

`sync` synchronizes. `publish` publishes. `undo` undoes. No flags to memorize. No arcane incantations. The same "for humans" thinking that shaped [Requests](/software/requests), applied to version control.

Many thanks to [Frost Ming](https://github.com/frostming) for maintaining this project.

## Install

```bash
$ uv pip install legit
```

Also available via Homebrew:

```bash
brew install legit
```

## Resources

- [Source Code on GitHub](https://github.com/frostming/legit)
- [Python Package Index](https://pypi.org/project/legit/)

## Related

- [**Requests**](/software/requests) — The library that established the "for humans" philosophy.
- [**Delegator**](/software/delegator) — Another tool for simplifying command-line interactions.
