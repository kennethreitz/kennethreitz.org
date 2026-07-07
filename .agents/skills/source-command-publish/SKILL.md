---
name: "source-command-publish"
description: "Publish the site to github"
---

# source-command-publish

Use this skill when the user asks to run the migrated source command `publish`.

## Command Template

Deploy the site to production.

Steps:
1. add all changes
2. Commit any pending changes
3. push to github

!git add -A && git commit -m "<insert commit message here>" || echo "No changes to commit"
!git push origin main
