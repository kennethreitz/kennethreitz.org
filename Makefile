init:
	uv sync

run:
	uv run uvicorn engine:api --host 0.0.0.0 --port 8000 --reload

docker-run:
	docker-compose up --build

build:
	docker compose build
