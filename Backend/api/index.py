# Vercel serverless function entry point
import sys
import os

# Add project root to Python path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from app.main import app

# Export FastAPI app directly - Vercel should handle ASGI apps natively
# If this doesn't work, Vercel may require Mangum for ASGI support
handler = app

