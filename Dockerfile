FROM astral/uv:python3.14-bookworm

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1

WORKDIR /app

# Install system dependencies for WeasyPrint (PDF generation)
RUN apt-get update && apt-get install -y \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    nginx \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files and required package files
COPY pyproject.toml README.md ./
COPY tuftecms ./tuftecms

# Install dependencies directly without creating a venv (since we're in a container)
RUN uv pip install . --system

# Copy the rest of the application
COPY . .

# Nginx config
COPY nginx.conf /etc/nginx/nginx.conf
COPY start.sh /app/start.sh
RUN chmod +x /app/start.sh && mkdir -p /var/cache/nginx

CMD ["/app/start.sh"]
