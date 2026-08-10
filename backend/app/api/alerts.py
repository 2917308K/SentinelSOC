from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.alert import Alert


router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"],
)


@router.get("/")
def get_alerts(
    db: Session = Depends(get_db),
):
    statement = (
        select(Alert)
        .order_by(Alert.created_at.desc())
    )

    alerts = db.scalars(statement).all()

    return alerts