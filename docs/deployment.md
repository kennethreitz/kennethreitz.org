# Deployment Guide

*Taking your TufteCMS site from development to production*

TufteCMS is designed to be deployed easily across various platforms while maintaining performance and reliability in production environments.

> **Production Readiness**: TufteCMS is experimental software. While functional, it may have undiscovered bugs or security considerations. Test thoroughly and monitor closely in production environments.

> This guide assumes you have a working site from [getting started](/docs/getting-started), organized content from [content structure](/docs/content-structure), and any desired customizations from the [customization guide](/docs/customization).

## Production Considerations

### Environment Configuration

Create a production configuration class:

```python
# config.py
import os
from pathlib import Path

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-change-in-production'
    DEBUG = False
    TESTING = False
    
    # Cache settings
    CACHE_TYPE = 'simple'  # or 'redis' for production
    CACHE_DEFAULT_TIMEOUT = 3600
    
    # Content settings
    DATA_DIR = Path('data')
    
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable must be set")
    
    # Production optimizations
    SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year for static files
```

### WSGI Application

Create a WSGI entry point:

```python
# wsgi.py
from tuftecms import create_app
from config import ProductionConfig

app = create_app(ProductionConfig)

if __name__ == "__main__":
    app.run()
```

### Requirements

Create production requirements:

```txt
# requirements.txt
flask>=2.0.0
markdown>=3.4.0
python-frontmatter>=1.0.0
gunicorn>=20.1.0  # WSGI server
gevent>=21.0.0    # Async support
```

Or with `uv`:

```toml
# pyproject.toml
[project]
dependencies = [
    "flask>=2.0.0",
    "markdown>=3.4.0", 
    "python-frontmatter>=1.0.0",
    "gunicorn>=20.1.0",
    "gevent>=21.0.0"
]
```

## Platform Deployment

### Traditional VPS/Server

#### Using Gunicorn + Nginx

1. **Install dependencies:**

```bash
# Install system packages
sudo apt update
sudo apt install nginx python3 python3-pip

# Install Python dependencies
pip install -r requirements.txt
```

2. **Configure Gunicorn:**

```python
# gunicorn_config.py
bind = "127.0.0.1:8000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
```

3. **Create systemd service:**

```ini
# /etc/systemd/system/tuftecms.service
[Unit]
Description=TufteCMS
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
RuntimeDirectory=tuftecms
WorkingDirectory=/var/www/tuftecms
Environment=FLASK_ENV=production
ExecStart=/var/www/tuftecms/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true

[Install]
WantedBy=multi-user.target
```

4. **Configure Nginx:**

```nginx
# /etc/nginx/sites-available/tuftecms
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    # Security headers
    add_header X-Frame-Options SAMEORIGIN;
    add_header X-Content-Type-Options nosniff;
    add_header X-XSS-Protection "1; mode=block";
    
    # Static files with long cache
    location /static/ {
        alias /var/www/tuftecms/tuftecms/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        gzip_static on;
    }
    
    # Application proxy
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Timeout settings
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

### Platform-as-a-Service

#### Heroku

1. **Create Procfile:**

```
web: gunicorn -c gunicorn_config.py wsgi:app
```

2. **Runtime specification:**

```
# runtime.txt
python-3.11
```

3. **Environment variables:**

```bash
heroku config:set SECRET_KEY=your-secret-key
heroku config:set FLASK_ENV=production
```

#### Railway

1. **Create railway.toml:**

```toml
[build]
builder = "NIXPACKS"

[deploy]
startCommand = "gunicorn -c gunicorn_config.py wsgi:app"
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

2. **Environment variables via Railway dashboard or CLI:**

```bash
railway variables set SECRET_KEY=your-secret-key
railway variables set FLASK_ENV=production
```

#### Fly.io

1. **Create fly.toml:**

```toml
app = "your-tuftecms-app"

[build]
  builder = "paketobuildpacks/builder:base"
  buildpacks = ["gcr.io/paketo-buildpacks/python"]

[env]
  FLASK_ENV = "production"
  PORT = "8080"

[[services]]
  http_checks = []
  internal_port = 8080
  protocol = "tcp"
  script_checks = []

  [services.concurrency]
    hard_limit = 25
    soft_limit = 20

  [[services.ports]]
    handlers = ["http"]
    port = 80
    force_https = true

  [[services.ports]]
    handlers = ["tls", "http"]
    port = 443

  [[services.tcp_checks]]
    grace_period = "1s"
    interval = "15s"
    restart_limit = 0
    timeout = "2s"
```

### Static Site Generation

For maximum performance, pre-generate static HTML:

```python
# generate_static.py
from tuftecms import create_app
from pathlib import Path
import os

def generate_static_site():
    """Generate static HTML files from TufteCMS content."""
    app = create_app()
    
    with app.app_context():
        # Get all content URLs
        from tuftecms.core.cache import get_blog_cache
        blog_data = get_blog_cache()
        
        output_dir = Path('static_build')
        output_dir.mkdir(exist_ok=True)
        
        # Generate homepage
        with app.test_client() as client:
            response = client.get('/')
            (output_dir / 'index.html').write_text(response.get_data(as_text=True))
            
            # Generate all content pages
            for post in blog_data['posts']:
                response = client.get(post['url'])
                if response.status_code == 200:
                    post_dir = output_dir / post['url'].strip('/')
                    post_dir.mkdir(parents=True, exist_ok=True)
                    (post_dir / 'index.html').write_text(response.get_data(as_text=True))
            
            # Generate index pages
            for endpoint in ['/archive', '/sidenotes', '/connections', '/search']:
                response = client.get(endpoint)
                if response.status_code == 200:
                    page_dir = output_dir / endpoint.strip('/')
                    page_dir.mkdir(parents=True, exist_ok=True)
                    (page_dir / 'index.html').write_text(response.get_data(as_text=True))

if __name__ == '__main__':
    generate_static_site()
```

Deploy static files to:
- **Netlify**: Drag and drop `static_build` folder
- **Vercel**: `vercel --prod static_build`
- **GitHub Pages**: Push to `gh-pages` branch
- **S3 + CloudFront**: Sync with `aws s3 sync`

## Performance Optimization

### Content Delivery

1. **Static asset optimization:**

```python
# In production config
SEND_FILE_MAX_AGE_DEFAULT = 31536000  # 1 year

# Compress assets
import gzip
from pathlib import Path

def compress_static_files():
    """Pre-compress static files for nginx gzip_static."""
    static_dir = Path('tuftecms/static')
    for file_path in static_dir.rglob('*'):
        if file_path.suffix in ['.css', '.js', '.html', '.svg']:
            with open(file_path, 'rb') as f_in:
                with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                    f_out.writelines(f_in)
```

2. **CDN configuration:**

```python
# For CloudFlare, AWS CloudFront, etc.
CDN_DOMAIN = 'https://cdn.your-domain.com'

@app.template_filter('cdn_url')
def cdn_url(filename):
    """Convert static URLs to CDN URLs."""
    if app.config.get('USE_CDN'):
        return f"{CDN_DOMAIN}/static/{filename}"
    return url_for('static', filename=filename)
```

### Caching Strategy

1. **Redis caching for production:**

```python
# Production config
import redis

CACHE_TYPE = 'redis'
CACHE_REDIS_URL = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')

# Initialize Redis cache
redis_client = redis.from_url(CACHE_REDIS_URL)
```

2. **Cache warming on deployment:**

```bash
# In your deployment script
python -c "
from tuftecms import create_app
from tuftecms.app import warm_caches
app = create_app()
with app.app_context():
    warm_caches()
"
```

### Database Considerations

TufteCMS is file-based, but for larger sites consider:

```python
# Optional: SQLite for search indexing
import sqlite3
from pathlib import Path

def create_search_index():
    """Create full-text search database."""
    db_path = Path('search_index.db')
    conn = sqlite3.connect(db_path)
    
    conn.execute('''
        CREATE VIRTUAL TABLE IF NOT EXISTS content_fts 
        USING fts5(title, content, url, tags)
    ''')
    
    # Populate from content cache
    # Implementation depends on your needs
    
    conn.close()
```

## Monitoring and Maintenance

### Health Checks

```python
# In blueprints/main.py
@main_bp.route('/health')
def health_check():
    """Comprehensive health check."""
    try:
        from ..core.cache import get_blog_cache
        blog_data = get_blog_cache()
        
        return jsonify({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'content_stats': blog_data.get('stats', {}),
            'version': '1.0.0'
        })
    except Exception as e:
        return jsonify({
            'status': 'unhealthy', 
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500
```

### Logging

```python
# In app.py
import logging
from logging.handlers import RotatingFileHandler

def configure_logging(app):
    """Configure production logging."""
    if not app.debug:
        # File handler
        file_handler = RotatingFileHandler(
            'logs/tuftecms.log', 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('TufteCMS startup')
```

### Backup Strategy

```bash
#!/bin/bash
# backup.sh - Content backup script

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups/tuftecms"
CONTENT_DIR="/var/www/tuftecms/data"

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup content with compression
tar -czf "$BACKUP_DIR/content_$DATE.tar.gz" -C "$CONTENT_DIR" .

# Keep only last 30 backups
find "$BACKUP_DIR" -name "content_*.tar.gz" -type f -mtime +30 -delete

# Optional: Upload to S3, rsync to remote server, etc.
# aws s3 cp "$BACKUP_DIR/content_$DATE.tar.gz" s3://your-backup-bucket/
```

## SSL/TLS Configuration

### Let's Encrypt with Certbot

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (add to cron)
0 12 * * * /usr/bin/certbot renew --quiet
```

### Security Headers

Add comprehensive security headers:

```nginx
# Security headers in nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options SAMEORIGIN;
add_header X-Content-Type-Options nosniff;
add_header X-XSS-Protection "1; mode=block";
add_header Referrer-Policy "strict-origin-when-cross-origin";
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline';";
```

## Post-Deployment

Once your site is live:

- **Monitor content growth** - Use insights from [content structure](/docs/content-structure) to organize new material effectively
- **Enhance with sidenotes** - Apply techniques from the [sidenotes guide](/docs/sidenotes) to add depth to your writing  
- **Iterate on design** - Use the [customization guide](/docs/customization) to refine your site's appearance and functionality
- **Return to documentation** - Explore the [documentation index](/docs) for advanced features and optimizations

---

*Deployment is where your contemplative digital garden meets the world. Choose platforms and configurations that align with your values - prioritize reader experience over metrics, privacy over tracking, sustainability over scale.*