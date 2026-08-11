from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.detection.engine import process_event
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse
from app.core.security import verify_agent_api_key

router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "/",
    response_model=EventResponse,
    dependencies=[Depends(verify_agent_api_key)],
)


def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
):
    db_event = Event(
        event_type=event.event_type,
        severity=event.severity,
        source=event.source,
        hostname=event.hostname,
        username=event.username,
        description=event.description,
        timestamp=event.timestamp,
        data=event.data,
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    process_event(
        db=db,
        event=db_event,
    )

    return db_event