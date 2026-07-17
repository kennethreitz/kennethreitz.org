FROM astral/uv:python3.14-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    MALLOC_ARENA_MAX=2

WORKDIR /app

# Install system dependencies for WeasyPrint (PDF generation) and the
# fortune command (powers /api/fortune). Debian bookworm no longer ships an
# English offensive set, so /api/fortune?offensive=1 degrades gracefully.
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    fortune-mod \
    fortunes \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files and required package files
COPY pyproject.toml README.md ./
COPY tuftecms ./tuftecms

# Install dependencies directly without creating a venv (since we're in a container)
RUN uv pip install . --system

# Copy the rest of the application
COPY . .

# Decode large source photographs once, sequentially, while building the image.
# Runtime requests should hit these immutable files instead of filling web-worker
# malloc arenas with concurrent Pillow buffers.
RUN python -B -m scripts.prebuild_media_cache

CMD ["granian", "--interface", "asgi", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--respawn-failed-workers", "--workers-max-rss", "768", "--workers-lifetime", "21600", "--static-path-route", "/static", "--static-path-mount", "tuftecms/static", "--static-path-expires", "604800", "engine:api"]
