from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.endpoint import Endpoint
from app.schemas.endpoint import (
    EndpointRegister,
    EndpointResponse,
)


router = APIRouter(
    prefix="/endpoints",
    tags=["Endpoints"],
)


@router.post(
    "/register",
    response_model=EndpointResponse,
)
def register_endpoint(
    endpoint: EndpointRegister,
    db: Session = Depends(get_db),
):
    existing_endpoint = db.scalar(
        select(Endpoint)
        .where(
            Endpoint.agent_id == endpoint.agent_id
        )
    )

    if existing_endpoint:

        existing_endpoint.hostname = endpoint.hostname
        existing_endpoint.operating_system = (
            endpoint.operating_system
        )
        existing_endpoint.architecture = endpoint.architecture
        existing_endpoint.status = "ONLINE"
        existing_endpoint.last_seen = datetime.now(
            timezone.utc
        )

        db.commit()
        db.refresh(existing_endpoint)

        return existing_endpoint

    new_endpoint = Endpoint(
        agent_id=endpoint.agent_id,
        hostname=endpoint.hostname,
        operating_system=endpoint.operating_system,
        architecture=endpoint.architecture,
        status="ONLINE",
    )

    db.add(new_endpoint)
    db.commit()
    db.refresh(new_endpoint)

    return new_endpoint


@router.get(
    "/",
    response_model=list[EndpointResponse],
)
def get_endpoints(
    db: Session = Depends(get_db),
):
    statement = (
        select(Endpoint)
        .order_by(Endpoint.last_seen.desc())
    )

    return db.scalars(statement).all()