"""
WSGI config for Railway deployment.
Pointe vers backend/wsgi.py
"""

import os
import sys

# Ajouter backend au PYTHONPATH
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

from backend.wsgi import application
