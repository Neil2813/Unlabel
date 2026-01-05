# Vercel serverless function entry point
import sys
import os
import traceback

# Add the project root to the Python path
# In Vercel, the working directory is typically the project root
# But we ensure the parent of api/ is in the path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))  # api/
project_root = os.path.dirname(current_dir)  # project root

# Add project root to path if not already there
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Suppress warnings about unused modules
import warnings
warnings.filterwarnings("ignore")

# Initialize handler variable
handler = None

try:
    # Import only what we need
    from mangum import Mangum
    
    # Import app after path is set
    from app.main import app
    
    # Create Mangum handler for Vercel
    # lifespan="off" disables lifespan events which can cause issues in serverless
    mangum_handler = Mangum(app, lifespan="off")
    
    # Wrap in a simple function to ensure Vercel can detect it properly
    def handler(event, context):
        return mangum_handler(event, context)
    
except ImportError as e:
    # Log import errors specifically
    error_msg = f"Import error: {str(e)}\n{traceback.format_exc()}"
    print(error_msg)
    
    # Create a minimal error handler that matches Vercel's expected format
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "Import failed", "details": "{str(e)}"}}'
        }
except Exception as e:
    # Log other errors
    error_msg = f"Failed to initialize app: {str(e)}\n{traceback.format_exc()}"
    print(error_msg)
    
    # Create a minimal error handler that matches Vercel's expected format
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": f'{{"error": "Initialization failed", "details": "{str(e)}"}}'
        }

# Ensure handler is always defined
if handler is None:
    def handler(event, context):
        return {
            "statusCode": 500,
            "headers": {"Content-Type": "application/json"},
            "body": '{"error": "Handler not initialized"}'
        }

