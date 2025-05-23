FROM python:3.12.4-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m pip install uv
RUN uv venv .venv
COPY pyproject.toml ./

RUN uv pip install .

WORKDIR /app

COPY . .
CMD ["uv", "run", "engine.py"]
