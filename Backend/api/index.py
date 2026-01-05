# Vercel serverless function entry point
# NOTE: This file is only used for Vercel deployment
# For Render/Railway/Fly.io, they use uvicorn directly (see render.yaml, Procfile, Dockerfile)

import sys
import os

# Add project root to Python path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from app.main import app

# Export FastAPI app directly
handler = app

