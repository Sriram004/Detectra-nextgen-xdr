from fastapi import APIRouter
from apps.api.app.db.repository import repo
from apps.api.app.schemas.models import Incident


router = APIRouter(prefix="/incidents", tags=["incidents"])


@router.get("", response_model=list[Incident])
def list_incidents() -> list[Incident]:
    return repo.list_incidents()
