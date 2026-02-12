from fastapi import APIRouter
from pydantic import BaseModel
from apps.api.app.db.repository import repo
from apps.api.app.schemas.models import Alert
from apps.api.app.services.alert_service import process_event, seed_demo_alert


router = APIRouter(prefix="/alerts", tags=["alerts"])


class EventIn(BaseModel):
    payload: dict


@router.get("", response_model=list[Alert])
def list_alerts() -> list[Alert]:
    return repo.list_alerts()


@router.post("/seed", response_model=Alert)
def seed_alert() -> Alert:
    return seed_demo_alert()


@router.post("/ingest")
def ingest_event(event: EventIn) -> dict:
    alerts = process_event(event.payload)
    return {"alerts_created": len(alerts), "alerts": [a.model_dump() for a in alerts]}
