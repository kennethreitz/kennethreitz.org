# Legit: The Sexy Git CLI

  [GitHub for Mac](http://mac.github.com/) is not just a Git client. This [comment](http://www.hackerne.ws/item?id=2684483) on Hacker News says it best:

 
> They haven't re\-created the git CLI tool in a GUI, they've created something different. They've created a tool that makes Git more accessible. Little things like auto\-stashing when you switch branches will confuse git veterans, but it will make Git much easier to grok for newcomers because of the assumptions it makes about your Git workflow.

 Why not bring this innovation back to the [command line Git interface](http://www.amazon.com/gp/product/1430218339/ref=as_li_ss_tl?ie=UTF8&amp;tag=bookforkind-20&amp;linkCode=as2&amp;camp=1789&amp;creative=390957&amp;creativeASIN=1430218339)?

 ## Enter Legit

 **Legit** is a new tool that allows you to interface with a Git respository much like you would with GitHub for Mac—from the command line.{{< sidenote >}}Legit represented an early attempt to bridge the usability gap between GUI and command-line Git tools. It introduced semantic commands like 'sprout' and 'graft' that made Git operations more intuitive for developers.{{< /sidenote >}}

 Switching branches becomes seamless. Any pending changes are automatically stashed and restored. Same goes with syncing your repository. And merging (grafting). And branching (sprouting).{{< sidenote >}}The organic metaphors of 'sprouting' for branching and 'grafting' for merging made Git's tree-like structure more intuitive by connecting version control to natural processes developers could easily visualize.{{< /sidenote >}}

 Managing remote branches becomes as simple as `publish branch` and `unpublish branch`. Simple.

 ## Installation

 Installing Legit is easy with pip (Python 2\.6 or 2\.7 required):

 
```
$ pip install legit
```
 This makes the `legit` command available. Run it within a repository.

 **Available commands**:

 * `sync [<branch>]` : Synchronizes the given branch. Defaults to current branch. Stash, Fetch, Auto-Merge/Rebase, Push, and Unstash.
* `branches` : Get a nice pretty list of available branches.
* `switch <branch>` : Switches to specified branch. Automatically stashes and unstashes any changes.
* `sprout [<branch>] <new-branch>` : Creates a new branch off of the specified branch. Defaults to current branch. Switches to it immediately.
* `graft <branch> <onto-branch>` : Merges specified branch into the second branch, and removes it. You can only graft unpublished branches.
* `publish <branch>` : Publishes specified branch to the remote.
* `unpublish <branch>` : Removes specified branch from the remote.

 ## Moving Forward

 **Legit** is very much in *beta*. I'm using it for real work already, so don't hesitate to try it out. As feedback and contributions come in, I expect the feature\-set to evolve. We'll see. That's up to you.

 Static binaries will be available soon for all major platforms.

 ## Source Code

 **Legit** is open source (BSD Licensed), powered by [Clint](https://github.com/kennethreitz/clint), [GitPython](http://pypi.python.org/pypi/GitPython/), and good intentions.

 * [Code on GitHub](https://github.com/kennethreitz/legit)

  