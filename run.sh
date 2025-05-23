#!/bin/bash
# Simple script to run the Kenneth Reitz blog engine

echo "🚀 Starting Kenneth Reitz Digital Vault & Blog..."
echo "📁 Serving content from: ./data/"
echo "🌐 Server will be available at: http://localhost:8000"
echo "🎨 Styled with Heroku colors"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

uv run python3 engine.py