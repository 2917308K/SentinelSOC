from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.detection.engine import process_event
from app.models.event import Event
from app.schemas.event import EventCreate, EventResponse


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)


@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
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
    )

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    process_event(
        db=db,
        event=db_event,
    )

    return db_event