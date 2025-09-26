from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#by creating SQLAlchemy engine  which connects to 
# the database and sesssion local factory inorder to create database session
#which exposes get_db() generator to be used as dependancy in FASTAPI routes. (Depends(get_db)), which gives a session and ensures it closes after use.