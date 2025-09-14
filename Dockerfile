FROM python:3.13-bookworm AS builder

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

RUN python -m pip install uv

# Copy dependency files first
COPY pyproject.toml ./

# Install dependencies directly without creating a venv (since we're in a container)
RUN uv pip install --system .

# Copy the rest of the application
COPY . .

# Run gunicorn directly (no need for uv run since we installed system-wide)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--worker-class", "gevent", "--workers", "4", "--worker-connections", "1000", "--timeout", "60", "engine:app"]
