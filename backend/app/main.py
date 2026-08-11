from fastapi import FastAPI

from app.api.alerts import router as alerts_router
from app.api.event import router as events_router
from app.core.database import Base, engine
from app.models import Alert, Event
from app.api.incidents import router as incidents_router
from app.api.endpoints import router as endpoints_router

Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="SentinelSOC API",
    description="Security monitoring and threat detection platform",
    version="0.2.0",
)


app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(incidents_router)
app.include_router(endpoints_router)

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "SentinelSOC API",
    }