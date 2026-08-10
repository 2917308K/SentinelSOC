from datetime import timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.detection.base import DetectionRule
from app.models.event import Event


class BruteForceRule(DetectionRule):
    rule_id = "AUTH_BRUTE_FORCE"
    name = "Authentication Brute Force"
    description = (
        "Detects repeated authentication failures "
        "from the same source within a short time window."
    )

    threshold = 5
    window_seconds = 60

    def evaluate(
        self,
        db: Session,
        event: Event,
    ) -> dict | None:

        if event.event_type != "AUTHENTICATION_FAILURE":
            return None

        window_start = event.timestamp - timedelta(
            seconds=self.window_seconds
        )

        statement = (
            select(func.count(Event.id))
            .where(
                Event.event_type == "AUTHENTICATION_FAILURE",
                Event.source == event.source,
                Event.hostname == event.hostname,
                Event.timestamp >= window_start,
                Event.timestamp <= event.timestamp,
            )
        )

        event_count = db.scalar(statement) or 0

        if event_count < self.threshold:
            return None

        return {
            "rule_id": self.rule_id,
            "alert_type": "BRUTE_FORCE",
            "base_score": 70,
            "event_count": event_count,
            "description": (
                f"Detected {event_count} failed authentication attempts "
                f"from source {event.source} within "
                f"{self.window_seconds} seconds."
            ),
        }