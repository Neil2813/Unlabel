from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

# Environment
# Auto-detect development environment if not explicitly set
if "ENV" not in os.environ:
    # Check if we're running locally (common development indicators)
    is_local = (
        os.path.exists(".git") or  # Git repository
        os.path.exists("pyproject.toml") or  # Local Python project
        "localhost" in os.getcwd().lower() or
        "projects" in os.getcwd().lower()
    )
    ENV = "development" if is_local else "production"
else:
    ENV = os.getenv("ENV", "production")

DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# API Keys with Fallback System
# Load all available Gemini API keys (GEMINI_API_KEY1 through GEMINI_API_KEY10)
GEMINI_API_KEYS: List[str] = []

# Try to load keys GEMINI_API_KEY1 through GEMINI_API_KEY10
for i in range(1, 11):
    key = os.getenv(f"GEMINI_API_KEY{i}", "")
    if key:
        GEMINI_API_KEYS.append(key)

# Also support single GEMINI_API_KEY for backward compatibility
single_key = os.getenv("GEMINI_API_KEY", "")
if single_key and single_key not in GEMINI_API_KEYS:
    GEMINI_API_KEYS.insert(0, single_key)

# Validate we have at least one key
if not GEMINI_API_KEYS:
    error_msg = """
    ╔════════════════════════════════════════════════════════════════╗
    ║          GEMINI API KEY CONFIGURATION ERROR                    ║
    ╟────────────────────────────────────────────────────────────────╢
    ║  No Gemini API keys found in environment variables.            ║
    ║                                                                ║
    ║  TO FIX:                                                       ║
    ║  1. Copy .env.example to .env in the Backend directory        ║
    ║  2. Add your Gemini API key(s):                                ║
    ║     GEMINI_API_KEY=your-api-key-here                          ║
    ║                                                                ║
    ║  You can get a free API key at:                                ║
    ║  https://makersuite.google.com/app/apikey                     ║
    ║                                                                ║
    ║  For production, consider adding multiple keys:                ║
    ║  GEMINI_API_KEY1=key1                                          ║
    ║  GEMINI_API_KEY2=key2                                          ║
    ║  ...for automatic failover.                                    ║
    ╚════════════════════════════════════════════════════════════════╝
    """
    
    if ENV == "production":
        raise ValueError(f"{error_msg}\\n\\nCannot start in PRODUCTION mode without API keys.")
    else:
        print(f"⚠️  WARNING: Running in DEVELOPMENT mode without API keys!")
        print(error_msg)
        print("\\n⚠️  AI features will not work. Please add API keys to enable them.\\n")

# For backward compatibility, set GEMINI_API_KEY to the first available key
GEMINI_API_KEY = GEMINI_API_KEYS[0] if GEMINI_API_KEYS else ""

if GEMINI_API_KEYS:
    print(f"✅ Loaded {len(GEMINI_API_KEYS)} Gemini API key(s) for fallback rotation")
    print(f"📍 Environment: {ENV}")
else:
    print(f"⚠️  Running without API keys in {ENV} mode")

# Frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://unlabel-eight.vercel.app")
