# api/index.py
import os
import sys

print("✅ [api/index.py] - Script start")

try:
    from mangum import Mangum

    print("✅ [api/index.py] - Imported Mangum")
except ImportError as e:
    print(f"❌ [api/index.py] - FAILED to import Mangum: {e}")
    sys.exit(1)


# Add the project root to the Python path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
print(f"✅ [api/index.py] - sys.path updated: {sys.path[0]}")

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
print(
    f"✅ [api/index.py] - DJANGO_SETTINGS_MODULE set to: {os.environ['DJANGO_SETTINGS_MODULE']}"
)

print("⏳ [api/index.py] - About to import Django ASGI application...")
try:
    from backend.asgi import application

    print("✅ [api/index.py] - Imported Django ASGI application")
except Exception as e:
    print(f"❌ [api/index.py] - FAILED to import application: {e}")
    sys.exit(1)


print("⏳ [api/index.py] - About to wrap application with Mangum...")
try:
    # Wrap the ASGI application with Mangum for Vercel's Lambda environment.
    app = Mangum(application, lifespan="off")
    print("✅ [api/index.py] - Wrapped application with Mangum")
except Exception as e:
    print(f"❌ [api/index.py] - FAILED to wrap with Mangum: {e}")
    sys.exit(1)

print("✅ [api/index.py] - Script end, 'app' is ready.")
