# Vercel serverless function entry point
import sys
import os

# Add project root to Python path
_backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _backend_dir not in sys.path:
    sys.path.insert(0, _backend_dir)

from mangum import Mangum
from app.main import app

# Create ASGI handler for Vercel
# Mangum converts FastAPI (ASGI) to AWS Lambda format that Vercel uses
adapter = Mangum(app, lifespan="off")

# Vercel expects handler to be a function, not a callable object
def handler(event, context):
    return adapter(event, context)

