---
description: Publish the site to github
allowed-tools: Bash(git:*)
---

Deploy the site to production.

Steps:
1. add all changes
2. Commit any pending changes
3. push to github

!git add -A && git commit -m "<insert commit message here>" || echo "No changes to commit"
!git push origin main
<!-- limit iexecution to 30s -->
!timeout 45 fly logs
