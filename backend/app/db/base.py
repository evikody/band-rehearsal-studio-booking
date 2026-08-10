from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """
    Every SQLAlchemy model inherits from this. Alembic's env.py imports
    Base.metadata to auto-generate migrations from whatever models exist.
    """
    pass
