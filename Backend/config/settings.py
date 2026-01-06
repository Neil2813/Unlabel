from dotenv import load_dotenv
import os
from typing import List

load_dotenv()

# Environment
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

# Validate we have at least one key in production
if not GEMINI_API_KEYS and ENV == "production":
    raise ValueError("At least one GEMINI_API_KEY is required in production (GEMINI_API_KEY or GEMINI_API_KEY1-10)")

# For backward compatibility, set GEMINI_API_KEY to the first available key
GEMINI_API_KEY = GEMINI_API_KEYS[0] if GEMINI_API_KEYS else ""

print(f"✅ Loaded {len(GEMINI_API_KEYS)} Gemini API key(s) for fallback rotation")

# Frontend URL for CORS
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://unlabel-eight.vercel.app")
