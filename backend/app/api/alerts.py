from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.database import get_db
from app.models.alert import Alert
from app.schemas.alert import AlertResponse


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get(
    "/",
    response_model=list[AlertResponse],
)
def get_alerts(
    db: Session = Depends(get_db),
):
    statement = (
        select(Alert)
        .options(selectinload(Alert.events))
        .order_by(Alert.created_at.desc())
    )

    return db.scalars(statement).all()