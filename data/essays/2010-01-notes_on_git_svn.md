# Notes on git-svn

  I'm forced to use SVN at the office. It's not THAT bad. OK, so maybe it's absolutely horrible. But it's more than understandable on their end.Those darn \`.svn\` folders drove me crazy. So, I use git\-svn. Git\-svn allows me to harness all the power of git with a subversion server.

> **Version Control Evolution**: This captures the 2010 enterprise landscape where SVN dominated corporate environments while Git was gaining traction among developers. The `.svn` folder complaint refers to SVN's practice of placing metadata folders in every directory, unlike Git's single `.git` folder. Git-svn was a crucial bridge technology during the SCM transition period.

 Perfect. (Or at least it's the best of a bad situation.)

 ### Setup

 \`git svn clone repo://url\`

 ### Commands

 \`git svn dcommit \-\-\` commit your changes\`git svn rebase \-\-\` update your working copy\`git stash \-\-\` stash your changes\`git stash apply \-\-\` take back your stash\`git stash clear \-\-\` clear the stash

 \#### See Also:

 \[svn2git](http://github.com/jcoglan/svn2git)
