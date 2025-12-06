# api/index.py
import os
import sys

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Get WSGI application
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()

# Vercel WSGI handler
app = application
