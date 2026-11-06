init:
	uv sync

test:
	uv run pytest

run:
	uv run granian --interface asgi --host 0.0.0.0 --port 8000 --reload engine:api

run-prod:
	uv run granian --interface asgi --host 0.0.0.0 --port 8000 --workers 4 engine:api

docker-run:
	docker-compose up --build

build:
	docker compose build

# Regenerate data/knowledge, data/library/books, and software History
# blocks from the Obsidian vault. Refuses to wipe knowledge if the vault
# looks partial. See scripts/vaultsync.py.
VAULT ?= $(HOME)/Notes
sync-vault:
	uv run python scripts/sync_vault.py --vault $(VAULT)
