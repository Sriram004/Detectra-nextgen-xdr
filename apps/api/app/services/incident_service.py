from uuid import uuid4
from apps.api.app.db.repository import repo
from apps.api.app.schemas.models import Alert, Incident


SEVERITY_TO_PRIORITY = {"low": 20, "medium": 50, "high": 75, "critical": 95}


def create_or_merge_incident(alert: Alert) -> Incident:
    related = [a for a in repo.list_alerts() if a.host_id == alert.host_id and a.status != "resolved"]
    if related:
        latest_incident = repo.list_incidents()[0] if repo.list_incidents() else None
        if latest_incident and alert.id not in latest_incident.alert_ids:
            latest_incident.alert_ids.append(alert.id)
            latest_incident.entities = sorted(set(latest_incident.entities + [alert.host_id]))
            repo.upsert_incident(latest_incident)
            return latest_incident

    incident = Incident(
        id=f"inc-{uuid4().hex[:8]}",
        title=f"Suspicious activity on {alert.host_id}",
        severity=alert.severity,
        priority=SEVERITY_TO_PRIORITY.get(alert.severity, 50),
        alert_ids=[alert.id],
        entities=[alert.host_id],
    )
    return repo.upsert_incident(incident)
