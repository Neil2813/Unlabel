# Vercel serverless function entry point
import sys
import os
import traceback

# Add the Backend directory to the Python path
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

try:
    from mangum import Mangum
    from app.main import app
    
    # Create Mangum handler for Vercel
    # lifespan="off" disables lifespan events which can cause issues in serverless
    handler = Mangum(app, lifespan="off")
except Exception as e:
    # Log the error for debugging
    error_msg = f"Failed to initialize app: {str(e)}\n{traceback.format_exc()}"
    print(error_msg)
    
    # Create a minimal error handler
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "Application initialization failed: {str(e)}"}}'
        }

