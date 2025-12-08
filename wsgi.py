"""
WSGI config for Railway deployment.
Pointe vers backend/wsgi.py
"""

import os
import sys

# Ajouter backend au PYTHONPATH
backend_path = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

# Importer l'application depuis backend/wsgi.py
from wsgi import application
