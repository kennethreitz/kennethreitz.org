"""Publish the vault into the site.

This is the historical command. It now runs the full sync: Knowledge,
the book shelf, and the software History blocks.

    $ uv run python scripts/import_knowledge.py --vault ~/Notes

Prefer ``scripts/sync_vault.py`` (or ``make sync-vault``). Both call the
same code. See that module's docstring for overrides, the privacy guard,
and why a partial vault will not wipe ``data/knowledge/``.
"""

import sys

from vaultsync import main

if __name__ == "__main__":
    sys.exit(main())
