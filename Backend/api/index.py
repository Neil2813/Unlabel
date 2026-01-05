# Vercel serverless function entry point
import sys
import os

# Add project root to Python path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

# Import dependencies
from mangum import Mangum
from app.main import app

# Create Mangum adapter
_adapter = Mangum(app, lifespan="off")

# Vercel handler function - must be named 'handler'
def handler(event, context):
    return _adapter(event, context)

