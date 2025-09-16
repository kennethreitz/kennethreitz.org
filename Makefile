init:
	uv sync

run:
	uv run gunicorn --bind 0.0.0.0 --worker-class gevent --workers 1 --worker-connections 1000 --timeout 60 engine:app

docker-run:
	docker-compose up --build

build:
	docker compose build
