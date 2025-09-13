# Notes on git-svn
*January 2010*

I'm forced to use SVN at the office. It's not THAT bad. OK, so maybe it's absolutely horrible. But it's more than understandable on their end. Those darn `.svn` folders drove me crazy. So, I use git-svn. Git-svn allows me to harness all the power of git with a subversion server.

Perfect. (Or at least it's the best of a bad situation.)

## Setup

```bash
git svn clone repo://url
```

## Commands

```bash
git svn dcommit  # commit your changes
git svn rebase   # update your working copy
git stash        # stash your changes
git stash apply  # take back your stash
git stash clear  # clear the stash
```

### See Also

[svn2git](https://github.com/nirvdrum/svn2git)