from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.studio import StudioUpdate, StudioRead
from app.services import studio_service

# Singleton resource: there is exactly one studio in this system, so the
# API has no id in the URL and no create/delete -- "create a second
# studio" and "delete the only studio" are not real operations here.
router = APIRouter(prefix="/api/studio", tags=["studio"])


@router.get("", response_model=StudioRead)
def get_studio(db: Session = Depends(get_db)):
    studio = studio_service.get_studio(db)
    if studio is None:
        # Only happens if the seed migration hasn't been run yet.
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Studio not configured yet -- run migrations",
        )
    return studio


@router.put("", response_model=StudioRead)
def update_studio(data: StudioUpdate, db: Session = Depends(get_db)):
    studio = studio_service.get_studio(db)
    if studio is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Studio not configured yet -- run migrations",
        )
    return studio_service.update_studio(db, studio, data)
