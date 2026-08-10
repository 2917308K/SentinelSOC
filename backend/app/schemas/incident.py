from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IncidentCreate(BaseModel):
    title: str
    description: str
    severity: str


class IncidentUpdate(BaseModel):
    status: str | None = None
    resolution: str | None = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str
    created_at: datetime
    updated_at: datetime
    resolution: str | None

    model_config = ConfigDict(from_attributes=True)