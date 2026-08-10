from sqlalchemy.orm import Session

from app.detection.risk import calculate_risk_score
from app.detection.rules import detect_brute_force
from app.models.alert import Alert
from app.models.event import Event


def process_event(
    db: Session,
    event: Event,
) -> Alert | None:
    detection = detect_brute_force(
        db=db,
        event=event,
    )

    if detection is None:
        return None

    risk_score = calculate_risk_score(
        base_score=detection["base_score"],
        event_count=detection["event_count"],
    )

    if risk_score >= 80:
        severity = "HIGH"
    elif risk_score >= 50:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    alert = Alert(
        rule_id=detection["rule_id"],
        alert_type=detection["alert_type"],
        severity=severity,
        risk_score=risk_score,
        source=event.source,
        hostname=event.hostname,
        description=detection["description"],
        event_count=detection["event_count"],
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert