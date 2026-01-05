# Vercel serverless function entry point
import sys
import os

# Add project root to Python path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from mangum import Mangum
from app.main import app

# Create Mangum adapter for FastAPI - must be at module level for Vercel detection
handler = Mangum(app, lifespan="off")

