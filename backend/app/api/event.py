from fastapi import APIRouter, Depends, status, HTTPException
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


@router.post(
    "/batch",
    response_model=list[EventResponse],
    dependencies=[Depends(verify_agent_api_key)],
)
def create_event_batch(
    events: list[EventCreate],
    db: Session = Depends(get_db),
):
    if len(events) > 100:
        raise HTTPException(
            status_code=413,
            detail="Maximum batch size is 100 events.",
        )

    if not events:
        return []

    db_events = [
        Event(
            event_type=event.event_type,
            severity=event.severity,
            source=event.source,
            hostname=event.hostname,
            username=event.username,
            description=event.description,
            timestamp=event.timestamp,
            data=event.data,
        )
        for event in events
    ]

    db.add_all(db_events)
    db.commit()

    for event in db_events:
        db.refresh(event)

    return db_events


@router.get("/", response_model=list[EventResponse])
def list_events(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Event).order_by(Event.timestamp.desc()).offset(skip).limit(limit).all()


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    event = db.get(Event, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    return event