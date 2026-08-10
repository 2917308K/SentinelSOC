from datetime import datetime, timedelta, timezone

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.event import Event


BRUTE_FORCE_RULE_ID = "AUTH_BRUTE_FORCE"

BRUTE_FORCE_THRESHOLD = 5

BRUTE_FORCE_WINDOW_SECONDS = 60


def detect_brute_force(
    db: Session,
    event: Event,
) -> dict | None:

    if event.event_type != "AUTHENTICATION_FAILURE":
        return None

    window_start = datetime.now(timezone.utc) - timedelta(
        seconds=BRUTE_FORCE_WINDOW_SECONDS
    )

    statement = (
        select(func.count(Event.id))
        .where(
            Event.event_type == "AUTHENTICATION_FAILURE",
            Event.source == event.source,
            Event.hostname == event.hostname,
            Event.timestamp >= window_start,
        )
    )

    event_count = db.scalar(statement) or 0

    if event_count < BRUTE_FORCE_THRESHOLD:
        return None

    return {
        "rule_id": BRUTE_FORCE_RULE_ID,
        "alert_type": "BRUTE_FORCE",
        "base_score": 70,
        "event_count": event_count,
        "description": (
            f"Detected {event_count} failed authentication attempts "
            f"from source {event.source} within "
            f"{BRUTE_FORCE_WINDOW_SECONDS} seconds."
        ),
    }