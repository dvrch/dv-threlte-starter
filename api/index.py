# api/index.py
import os
import sys

from mangum import Mangum

# Add the project root to the Python path.
# The project root is one level up from the 'api' directory.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Import the Django ASGI application.
from backend.asgi import application

# Wrap the ASGI application with Mangum for Vercel's Lambda environment.
# 'lifespan="off"' is recommended for Django apps on Lambda to avoid issues
# with startup/shutdown signals.
app = Mangum(application, lifespan="off")
