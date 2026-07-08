import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

ENV_PATH = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=ENV_PATH)

raw_database_url = os.getenv("DATABASE_URL")
if not raw_database_url:
    raise ValueError("DATABASE_URL is not set. Check environment or backend/.env file.")

# Render/Postgres can sometimes use postgres://; SQLAlchemy expects postgresql://
if raw_database_url.startswith("postgres://"):
    DATABASE_URL = raw_database_url.replace("postgres://", "postgresql://", 1)
else:
    DATABASE_URL = raw_database_url

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()