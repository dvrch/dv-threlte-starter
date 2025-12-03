"""
WSGI config for films_backend project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Get the project root (parent of backend/)
PROJECT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_DIR))

# Load .env from project root (works both locally and on Vercel)
env_file = PROJECT_DIR / '.env'
if env_file.exists():
    load_dotenv(env_file)
else:
    # Fallback for Vercel (where .env might not exist, vars come from Dashboard)
    load_dotenv()

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

application = get_wsgi_application()
