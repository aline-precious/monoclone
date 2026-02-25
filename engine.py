"""Database engine, session factory, and dependency for FastAPI routes."""

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.core.config import settings


# ─── Engine ────────────────────────────────────────────────────────────────────
# pool_pre_ping=True checks the connection is alive before using it.
# This prevents errors when the DB drops idle connections.
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,           # max persistent connections in the pool
    max_overflow=20,        # extra connections allowed under heavy load
    echo=settings.DEBUG,    # logs all SQL statements when DEBUG=True
)


# ─── Session Factory ───────────────────────────────────────────────────────────
# autocommit=False — we control when to commit, nothing saves by accident
# autoflush=False  — we control when SQLAlchemy syncs changes to the DB
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# ─── Dependency ────────────────────────────────────────────────────────────────
def get_db() -> Generator[Session, None, None]:
    """
    FastAPI dependency that provides a database session per request.

    Usage in a route:
        @router.get("/customers")
        def list_customers(db: Session = Depends(get_db)):
            ...

    Guarantees the session is always closed after the request,
    even if an exception is raised.
    """
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
