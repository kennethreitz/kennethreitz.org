"""Application factory for TufteCMS."""

import os
from pathlib import Path

# Enable gevent async I/O optimizations
import gevent
from gevent import monkey

from flask import Flask

from .blueprints import api_bp, content_bp, feeds_bp, main_bp
from .config import Config

monkey.patch_all()  # Patch standard library for async I/O


def warm_caches():
    """Warm up all caches at application startup."""
    print("🔥 Starting background cache warming...")
    try:
        from .core.cache import (
            get_blog_cache,
            get_connections_cache,
            get_outlines_cache,
            get_quotes_cache,
            get_sidenotes_cache,
            get_terms_cache,
        )

        # Load all caches
        blog_data = get_blog_cache()
        sidenotes_data = get_sidenotes_cache()
        outlines_data = get_outlines_cache()
        quotes_data = get_quotes_cache()
        connections_data = get_connections_cache()
        terms_data = get_terms_cache()

        # Print cache statistics
        print(f"✅ Blog cache: {blog_data['stats']['total_posts']} posts loaded")
        print(f"✅ Sidenotes cache: {sidenotes_data['stats']['total_sidenotes']} sidenotes from {sidenotes_data['stats']['total_articles']} articles")
        print(f"✅ Outlines cache: {outlines_data['stats']['total_headings']} headings from {outlines_data['stats']['total_articles']} articles")
        print(f"✅ Quotes cache: {quotes_data['stats']['total_quotes']} quotes from {quotes_data['stats']['total_articles']} articles")
        print(f"✅ Connections cache: {connections_data['stats']['total_outgoing']} outgoing, {connections_data['stats']['total_incoming']} incoming connections")
        print(f"✅ Terms cache: {terms_data['stats']['total_terms']} terms with {terms_data['stats']['total_references']} references")
        print("🚀 All caches warmed up successfully!")

    except Exception as e:
        print(f"❌ Error warming caches: {e}")
        # Don't fail startup if cache warming fails
        import traceback
        traceback.print_exc()


def warm_caches_background(app):
    """Warm up caches in background thread."""
    import threading
    
    def cache_worker():
        with app.app_context():
            warm_caches()
    
    # Start cache warming in background thread
    cache_thread = threading.Thread(target=cache_worker, daemon=True)
    cache_thread.start()
    print("🚀 Server starting... (caches warming in background)")


def create_app(config_class=Config):
    """Create and configure the Flask application."""
    # Get absolute paths for directories
    base_dir = Path(__file__).parent.parent
    template_dir = base_dir / "templates"
    static_dir = base_dir / "static"

    app = Flask(
        __name__,
        template_folder=str(template_dir),
        static_folder=str(static_dir),
        static_url_path="/static",
    )
    app.config.from_object(config_class)

    # Register template filters
    register_template_filters(app)

    # Register context processors
    register_context_processors(app)

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(content_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(feeds_bp)

    # Warm up caches in background
    warm_caches_background(app)

    return app


def register_template_filters(app):
    """Register custom Jinja2 template filters."""

    @app.template_filter("strftime")
    def strftime_filter(date, fmt="%Y-%m-%d"):
        """Format a datetime object using strftime."""
        from datetime import datetime

        if date is None:
            return ""
        if isinstance(date, str) and date.lower() == "now":
            date = datetime.now()
        return date.strftime(fmt)

    @app.template_filter("unescape")
    def unescape_filter(text):
        """Unescape HTML entities in text."""
        import html

        if text is None:
            return ""
        return html.unescape(text)


def register_context_processors(app):
    """Register context processors to inject data into all templates."""

    @app.context_processor
    def inject_index_counts():
        """Make index counts available to all templates."""
        try:
            # Import here to avoid circular imports
            from .core.cache import (
                get_connections_cache,
                get_outlines_cache,
                get_quotes_cache,
                get_sidenotes_cache,
                get_terms_cache,
            )

            # Get actual cache data
            sidenotes_data = get_sidenotes_cache()
            outlines_data = get_outlines_cache()
            quotes_data = get_quotes_cache()
            connections_data = get_connections_cache()
            terms_data = get_terms_cache()

            return {
                "index_counts": {
                    "sidenotes": sidenotes_data["stats"].get("total_sidenotes", 0),
                    "outlines": outlines_data["stats"].get("total_headings", 0),
                    "quotes": quotes_data["stats"].get("total_quotes", 0),
                    "connections_outgoing": connections_data["stats"].get(
                        "total_outgoing", 0
                    ),
                    "connections_incoming": connections_data["stats"].get(
                        "total_incoming", 0
                    ),
                    "terms": terms_data["stats"].get("total_terms", 0),
                    "terms_total_refs": terms_data["stats"].get("total_references", 0),
                }
            }
        except Exception as e:
            print(f"Error getting index counts: {e}")
            # Fallback to prevent template errors
            return {
                "index_counts": {
                    "sidenotes": 0,
                    "outlines": 0,
                    "quotes": 0,
                    "connections_outgoing": 0,
                    "connections_incoming": 0,
                    "terms": 0,
                    "terms_total_refs": 0,
                }
            }

    @app.after_request
    def add_immediate_visibility(response):
        """Add script to immediately show content to prevent invisible page."""
        if response.content_type and "text/html" in response.content_type:
            # Inject a script right after <head> to immediately show content
            content = response.get_data(as_text=True)
            if "<head>" in content and "visibility: hidden" in content:
                # Add script to immediately show content
                immediate_script = """<script>
                    // Immediately show content to prevent invisible page
                    document.documentElement.classList.add('loaded');
                </script>"""
                content = content.replace("<head>", "<head>" + immediate_script)
                response.set_data(content)
        return response
