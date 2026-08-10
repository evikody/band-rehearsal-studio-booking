from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict


class StudioBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    description: str | None = Field(default=None, max_length=1000)
    price_per_hour: float = Field(gt=0, description="Must be greater than zero")


class StudioCreate(StudioBase):
    """What the client sends to create a studio. No id, no created_at --
    those are server-assigned, never client-supplied."""
    pass


class StudioUpdate(StudioBase):
    """What the client sends to replace a studio's fields (PUT).
    Same shape as create -- a full replace, not a partial patch."""
    pass


class StudioRead(StudioBase):
    """What the server sends back. Includes the server-assigned fields."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
