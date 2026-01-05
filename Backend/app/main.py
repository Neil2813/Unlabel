from fastapi import FastAPI

app = FastAPI(
    title="AI-Native Food Intelligence Backend"
)

# Import routers after app creation to avoid circular imports
try:
    from app.ai.router import router as ai_router
    from app.food.router import router as food_router
except ImportError as e:
    import traceback
    print(f"Failed to import routers: {e}")
    print(traceback.format_exc())
    # Create empty routers to prevent crash
    from fastapi import APIRouter
    ai_router = APIRouter()
    food_router = APIRouter()

from fastapi.middleware.cors import CORSMiddleware

# CORS configuration - allow frontend domain
import os
FRONTEND_URL = os.getenv("FRONTEND_URL", "https://unlabel-eight.vercel.app")
ALLOWED_ORIGINS = [
    FRONTEND_URL,
    "https://unlabel-eight.vercel.app",
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint (no dependencies)
@app.get("/")
@app.get("/api/health")
def health_check():
    return {"status": "ok", "message": "API is running"}

app.include_router(ai_router, prefix="/api")
app.include_router(food_router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
