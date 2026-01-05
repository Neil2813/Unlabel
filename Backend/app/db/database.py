from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config.settings import DATABASE_URL
import os

# For SQLite, adjust connection args based on environment
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}
    # In serverless environments, use in-memory or /tmp for SQLite
    if os.getenv("ENV") == "production" and "/tmp" not in DATABASE_URL:
        # Use /tmp directory for SQLite in serverless (Vercel)
        db_path = DATABASE_URL.replace("sqlite:///", "")
        if not db_path.startswith("/tmp") and not os.path.exists(os.path.dirname(db_path)):
            # Use /tmp as fallback
            db_name = os.path.basename(db_path) if db_path else "food_intelligence.db"
            DATABASE_URL = f"sqlite:////tmp/{db_name}"

engine = create_engine(
    DATABASE_URL, connect_args=connect_args
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
