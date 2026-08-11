from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EventCreate(BaseModel):
    event_type: str
    severity: str = "LOW"
    source: str
    hostname: str
    username: str | None = None
    description: str
    timestamp: datetime | None = None
    data: dict | None = None


class EventResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    source: str
    hostname: str
    username: str | None
    description: str
    timestamp: datetime
    data: dict | None = None
    model_config = ConfigDict(from_attributes=True)