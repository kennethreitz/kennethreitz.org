"""Sync the Obsidian vault into the site.

    $ uv run python scripts/sync_vault.py --vault ~/Notes
    $ uv run python scripts/sync_vault.py --vault ~/Notes --dry-run
    $ uv run python scripts/sync_vault.py --vault ~/Notes --check

See ``vaultsync.py`` for the override layer, the privacy guard, and the
Knowledge / Books / software History split.
"""

import sys

from vaultsync import main

if __name__ == "__main__":
    sys.exit(main())
