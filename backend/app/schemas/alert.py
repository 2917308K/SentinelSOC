from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertEventResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    source: str
    hostname: str
    username: str | None
    description: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class AlertResponse(BaseModel):
    id: int
    rule_id: str
    alert_type: str
    severity: str
    risk_score: int
    source: str
    hostname: str
    description: str
    status: str
    event_count: int
    created_at: datetime
    events: list[AlertEventResponse]

    model_config = ConfigDict(from_attributes=True)