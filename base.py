"""SQLAlchemy declarative base shared across all ORM models."""

from sqlalchemy.orm import declarative_base, DeclarativeBase


class Base(DeclarativeBase):
    """
    Base class for all database models.

    All models inherit from this:
        class Customer(Base): ...
        class Order(Base): ...

    This centralizes table metadata so that:
        Base.metadata.create_all(bind=engine)
    creates all tables in one call on startup.
    """
