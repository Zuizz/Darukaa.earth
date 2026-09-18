from collections.abc import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings

# Normalize postgres:// scheme if provided by hosted platforms
runtime_db_url = settings.DATABASE_URL
if runtime_db_url.startswith("postgres://"):
    runtime_db_url = runtime_db_url.replace("postgres://", "postgresql://", 1)

# Pooled connection engine for runtime queries
engine = create_engine(
    runtime_db_url,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
    pool_recycle=1800,
    pool_timeout=30,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
