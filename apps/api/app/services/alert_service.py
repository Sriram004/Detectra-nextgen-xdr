from uuid import uuid4
from apps.api.app.db.repository import repo
from apps.api.app.schemas.models import Alert
from apps.api.app.services.incident_service import create_or_merge_incident
from services.detection.rule_engine.sigma_loader import SigmaLoader
from services.detection.rule_engine.evaluator import match_sigma_rule


def process_event(event: dict) -> list[Alert]:
    loader = SigmaLoader()
    alerts: list[Alert] = []

    for rule in loader.load_all():
        if match_sigma_rule(rule, event):
            alert = Alert(
                id=f"al-{uuid4().hex[:10]}",
                rule_id=rule.get("id", "unknown-rule"),
                title=rule.get("title", "Detection match"),
                severity=rule.get("level", "medium"),
                host_id=event.get("host", {}).get("id", "unknown-host"),
                user_id=event.get("user", {}).get("id"),
                confidence=0.8,
            )
            repo.upsert_alert(alert)
            create_or_merge_incident(alert)
            alerts.append(alert)

    return alerts


def seed_demo_alert() -> Alert:
    alert = Alert(
        id="al-demo-001",
        rule_id="suspicious_powershell_encoded",
        title="Suspicious PowerShell Encoded Command",
        severity="high",
        host_id="host-01",
        confidence=0.9,
    )
    repo.upsert_alert(alert)
    create_or_merge_incident(alert)
    return alert
