from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EndpointRegister(BaseModel):
    agent_id: str
    hostname: str
    operating_system: str
    architecture: str


class EndpointResponse(BaseModel):
    id: int
    agent_id: str
    hostname: str
    operating_system: str
    architecture: str
    status: str
    last_seen: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)