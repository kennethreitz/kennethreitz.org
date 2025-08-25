# GitHub Syncer in Python

  Today I rewrote a little utility I've been using for a while to keep all of my GitHub repos up to date and organized. It updates / clones all private, public, and watched repositories from your account. It also detects if your repo is a mirror or fork, and files it accordingly.My watched list is huge, but I like to have a local copy of my favorite libraries. You never know if the owner will take it down, or worse, move it to another SCM! ;\-)

> **Historical Context**: This was written during GitHub's early expansion period (2010), when developers were still concerned about platform stability and vendor lock-in. The fear of projects "moving to another SCM" reflects the SCM wars era when Git, SVN, and Mercurial competed. The emphasis on local backups shows a decentralized mindset common among early Git adopters.

 The script depends on the \*\*GitHub2\*\* module. If you don't have it, you can install it easily.

  $ pip install github2

 I recommend running this from \`\~/repos/\`.

 [http://gist.github.com/619473\.js?file\=sync.py](http://gist.github.com/619473.js?file=sync.py)

 
```
#!/usr/bin/env python# -*- coding: utf-8 -*-"""Kenneth Reitz's GitHub SyncerThis script uses the GitHub API to get a list of all forked, mirrored, public, andprivate repos in your GitHub account. If the repo already exists locally, it willupdate it via git-pull. Otherwise, it will properly clone the repo.It will organize your repos into the following directory structure:+ repos├── forks (public fork repos)├── mirrors (public mirror repos)├── private (private repos)├── public (public repos)├── watched (this script)└── sync.py (this script)Requires Ask Solem's github2 (http://pypi.python.org/pypi/github2).Inspired by Gisty (http://github.com/swdyh/gisty)."""import osfrom commands import getoutput as cmdfrom github2.client import Github# GitHub configurationsGITHUB_USER = cmd('git config github.user')GITHUB_TOKEN = cmd('git config github.token')

> **Security Note**: This approach stores API tokens in git config, which was a common but insecure practice in 2010. Modern best practices recommend environment variables or dedicated credential managers. The GitHub API has since moved to more sophisticated authentication methods.# API Objectgithub = Github(username=GITHUB_USER, api_token=GITHUB_TOKEN)# repo slotsrepos = {}repos['watched'] = [r for r in github.repos.watching(GITHUB_USER)]repos['private'] = []repos['mirrors'] = []repos['public'] = []repos['forks'] = []# Collect GitHub repos via APIfor repo in github.repos.list():if repo.private:repos['private'].append(repo)elif repo.fork:repos['forks'].append(repo)elif 'mirror' in repo.description.lower():# mirrors owned by self if mirror in description...repos['mirrors'].append(repo)else:repos['public'].append(repo)for org, repos in repos.iteritems():for repo in repos:# create org directory (safely)try:os.makedirs(org)except OSError:pass# enter org diros.chdir(org)# I own the repoprivate = True if org in ('private', 'fork', 'mirror') else False# just `git pull` if it's already thereif os.path.exists(repo.name):os.chdir(repo.name)print('Updating repo: %s' % (repo.name))os.system('git pull')os.chdir('..')else:if private:print('Cloning private repo: %s' % (repo.name))os.system('git clone git@github.com:%s/%s.git' % (repo.owner, repo.name))else:print('Cloning repo: %s' % (repo.name))os.system('git clone git://github.com/%s/%s.git' % (repo.owner, repo.name))# return to baseos.chdir('..')print
```
 \[Source on GitHub](http://gist.github.com/619473\)

 Enjoy!

  