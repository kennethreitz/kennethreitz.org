FROM python:3.12.4-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
WORKDIR /app

RUN python -m pip install uv
RUN uv venv .venv
COPY requirements.txt ./


RUN uv pip install .


FROM python:3.12.4-slim-bookworm

WORKDIR /app
COPY --from=builder /app/.venv .venv/

COPY . .
CMD ["/app/.venv/bin/fastapi", "run", "tuftedoc.py"]
