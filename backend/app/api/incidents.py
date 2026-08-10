from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.incident import Incident
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
    IncidentUpdate,
)


router = APIRouter(
    prefix="/incidents",
    tags=["Incidents"],
)


@router.post(
    "/",
    response_model=IncidentResponse,
)
def create_incident(
    incident: IncidentCreate,
    db: Session = Depends(get_db),
):
    new_incident = Incident(
        title=incident.title,
        description=incident.description,
        severity=incident.severity,
    )

    db.add(new_incident)
    db.commit()
    db.refresh(new_incident)

    return new_incident


@router.get(
    "/",
    response_model=list[IncidentResponse],
)
def get_incidents(
    db: Session = Depends(get_db),
):
    statement = (
        select(Incident)
        .order_by(Incident.created_at.desc())
    )

    return db.scalars(statement).all()


@router.patch(
    "/{incident_id}",
    response_model=IncidentResponse,
)
def update_incident(
    incident_id: int,
    update: IncidentUpdate,
    db: Session = Depends(get_db),
):
    incident = db.get(
        Incident,
        incident_id,
    )

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found",
        )

    if update.status is not None:
        incident.status = update.status

    if update.resolution is not None:
        incident.resolution = update.resolution

    incident.updated_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(incident)

    return incident