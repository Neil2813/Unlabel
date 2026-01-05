# Vercel serverless function entry point
import sys
import os

# Add the Backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, backend_dir)

from app.main import app

# Vercel Python runtime automatically handles ASGI apps
# Just export the app instance

