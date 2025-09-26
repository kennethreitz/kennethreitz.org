#!/usr/bin/env python
"""
TufteCMS Engine - Main application entry point.

This file serves as the entry point for the TufteCMS application.
All the core functionality has been modularized into the tuftecms package.
"""

import os
from tuftecms import create_app

# Create the Flask application using the factory pattern
app = create_app()

if __name__ == "__main__":
    # Run the development server
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=True, host="0.0.0.0", port=port)
