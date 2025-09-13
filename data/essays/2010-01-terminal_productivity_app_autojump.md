# Terminal Productivity App: AutoJump
*January 2010*

On average, I'd say I spend 65% of the workday in a terminal session. About 95% of that time is within the same 4 directories. `cd foo` & `cd bar` can get old.

**AutoJump** is a "cd command that learns". It tracks shell history to detect which directories you spend the most time in, and allows you to *jump* to them without any directory context. It even supports Zsh tab completion. :)

From this:
```bash
$ cd /Users/kreitz/repos/public/gistapi
```

To this:
```bash
$ j gistapi
```

Life is good.

**Links:**
- [Project Page](http://wiki.github.com/joelthelion/autojump/)
- [Source on GitHub](http://github.com/joelthelion/autojump)