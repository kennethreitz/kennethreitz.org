#!/bin/sh
# Start Granian on port 8001 (behind nginx)
granian --interface asgi --host 127.0.0.1 --port 8001 --workers 4 engine:api &

# Start nginx on port 8000 (public-facing)
nginx -g 'daemon off;'
