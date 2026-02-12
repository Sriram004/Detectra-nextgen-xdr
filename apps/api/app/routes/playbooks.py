from pathlib import Path
import yaml
from fastapi import APIRouter, Depends, HTTPException
from apps.api.app.auth.deps import require_role
from apps.api.app.db.repository import repo
from apps.api.app.schemas.models import PlaybookRunRequest
from services.response_engine.playbook_runner import run_playbook


router = APIRouter(prefix="/playbooks", tags=["playbooks"])


@router.post("/run", dependencies=[Depends(require_role({"admin", "responder"}))])
def run_playbook_for_alert(payload: PlaybookRunRequest) -> dict:
    alert = repo.alerts.get(payload.alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")

    playbook_path = Path("rules/playbooks/contain_suspicious_powershell.yml")
    with playbook_path.open("r", encoding="utf-8") as handle:
        playbook = yaml.safe_load(handle)

    steps = run_playbook(playbook, alert.model_dump())
    return {"playbook": playbook.get("name"), "steps": steps}
