#!/usr/bin/env python
"""
TufteCMS Engine - Main application entry point.

This file serves as the entry point for the TufteCMS application.
All the core functionality has been modularized into the tuftecms package.
"""

import os
from asgiref.wsgi import WsgiToAsgi
from tuftecms import create_app

# Create the Flask application using the factory pattern
flask_app = create_app()

# Wrap Flask WSGI app for ASGI compatibility (uvicorn)
app = WsgiToAsgi(flask_app)

if __name__ == "__main__":
    # Run the development server
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("engine:app", host="0.0.0.0", port=port, reload=True)
