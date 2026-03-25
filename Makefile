init:
	uv sync

run:
	uv run granian --interface asgi --host 0.0.0.0 --port 8000 --reload engine:api

run-prod:
	uv run granian --interface asgi --host 0.0.0.0 --port 8000 --workers 4 engine:api

docker-run:
	docker-compose up --build

build:
	docker compose build
