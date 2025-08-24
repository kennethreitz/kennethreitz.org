# Docker Setup for Kenneth Reitz's Site

This project includes Docker Compose setup for easy local development.

## Prerequisites

- Docker
- Docker Compose

## Quick Start

1. **Build and run the application:**
   ```bash
   docker-compose up --build
   ```

2. **Access the site:**
   Open your browser to http://localhost:8000

3. **Stop the application:**
   ```bash
   docker-compose down
   ```

## Development Mode

The Docker Compose setup includes:

- **Hot reloading:** Changes to your code will automatically reload the server
- **Volume mapping:** Your local files are mapped into the container
- **Debug mode:** Flask debug mode is enabled for development

## Useful Commands

- **Run in background:** `docker-compose up -d`
- **View logs:** `docker-compose logs -f web`
- **Rebuild:** `docker-compose up --build`
- **Shell access:** `docker-compose exec web bash`

## Environment Variables

The following environment variables are set for development:

- `FLASK_ENV=development`
- `FLASK_DEBUG=1`

## Alternative: Direct Python Execution

If you prefer not to use Docker, you can still run the site directly:

```bash
# Install dependencies
uv sync

# Run the application
uv run python3 engine.py
```

The site will be available at http://localhost:8000