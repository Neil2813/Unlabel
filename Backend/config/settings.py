from dotenv import load_dotenv
import os

load_dotenv()

# Environment
ENV = os.getenv("ENV", "production")
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# API Keys
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
if not GEMINI_API_KEY and ENV == "production":
    raise ValueError("GEMINI_API_KEY is required in production")

# Frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://unlabel-eight.vercel.app")
