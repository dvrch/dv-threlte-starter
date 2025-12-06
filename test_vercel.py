#!/usr/bin/env python3
"""
Test script for Vercel WSGI deployment
"""

import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "."))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Initialize Django
import django

django.setup()

# Get WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

if __name__ == "__main__":
    from wsgiref.simple_server import make_server

    print("Starting Django WSGI server on http://localhost:8000")
    print("Test URLs:")
    print("  - http://localhost:8000/health/")
    print("  - http://localhost:8000/api/geometries/")
    print("  - http://localhost:8000/admin/")
    httpd = make_server("localhost", 8000, application)
    httpd.serve_forever()
