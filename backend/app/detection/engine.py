from sqlalchemy import select
from sqlalchemy.orm import Session

from app.detection.registry import get_detection_rules
from app.detection.risk import calculate_risk_score
from app.models.alert import Alert
from app.models.event import Event


def process_event(
    db: Session,
    event: Event,
) -> list[Alert]:

    alerts: list[Alert] = []

    rules = get_detection_rules()

    for rule in rules:

        detection = rule.evaluate(
            db=db,
            event=event,
        )

        if detection is None:
            continue

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

        existing_alert = db.scalar(
            select(Alert)
            .where(
                Alert.rule_id == detection["rule_id"],
                Alert.source == event.source,
                Alert.hostname == event.hostname,
                Alert.status == "OPEN",
            )
            .limit(1)
        )

        if existing_alert:

            existing_alert.event_count = detection["event_count"]
            existing_alert.risk_score = risk_score
            existing_alert.severity = severity
            existing_alert.description = detection["description"]

            alerts.append(existing_alert)

        else:

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
            alerts.append(alert)

    if alerts:
        db.commit()

        for alert in alerts:
            db.refresh(alert)

    return alerts