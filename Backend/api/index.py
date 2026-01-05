# Vercel serverless function entry point
import sys
import os

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import and setup
from mangum import Mangum
from app.main import app

# Create Mangum handler - Vercel will call this handler function
mangum_instance = Mangum(app, lifespan="off")

# Export handler as a simple function wrapper
def handler(event, context):
    """Vercel serverless function handler"""
    return mangum_instance(event, context)

