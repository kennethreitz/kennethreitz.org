FROM astral/uv:python3.13-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Copy dependency files first
COPY pyproject.toml ./

# Install dependencies directly without creating a venv (since we're in a container)
RUN uv sync

# Copy the rest of the application
COPY . .

# Run gunicorn directly (no need for uv run since we installed system-wide)
CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8000", "--worker-class", "gevent", "--workers", "1", "--worker-connections", "1000", "--timeout", "60", "engine:app"]
