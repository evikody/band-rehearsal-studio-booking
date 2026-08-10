from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """
    FastAPI dependency that provides one database session per request.
    The 'yield' pattern guarantees db.close() runs even if the request
    raises an exception -- we never leak an open connection.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
