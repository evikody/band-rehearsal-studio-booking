from sqlalchemy.orm import Session

from app.models.studio import Studio
from app.schemas.studio import StudioCreate, StudioUpdate


def get_studio(db: Session) -> Studio | None:
    """There is exactly one studio row. .first() is correct here, not a
    shortcut -- there is no 'which one' to disambiguate."""
    return db.query(Studio).first()


def update_studio(db: Session, studio: Studio, data: StudioUpdate) -> Studio:
    for field, value in data.model_dump().items():
        setattr(studio, field, value)
    db.commit()
    db.refresh(studio)
    return studio


def create_studio(db: Session, data: StudioCreate) -> Studio:
    """Not exposed via the API -- only used once, by the seed migration,
    to create the single studio row that this system will ever have."""
    studio = Studio(**data.model_dump())
    db.add(studio)
    db.commit()
    db.refresh(studio)
    return studio
