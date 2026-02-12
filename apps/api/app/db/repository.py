from collections import defaultdict
from apps.api.app.schemas.models import Alert, Incident


class InMemoryRepository:
    def __init__(self) -> None:
        self.alerts: dict[str, Alert] = {}
        self.incidents: dict[str, Incident] = {}
        self.host_alert_index: dict[str, list[str]] = defaultdict(list)

    def upsert_alert(self, alert: Alert) -> Alert:
        self.alerts[alert.id] = alert
        if alert.id not in self.host_alert_index[alert.host_id]:
            self.host_alert_index[alert.host_id].append(alert.id)
        return alert

    def list_alerts(self) -> list[Alert]:
        return sorted(self.alerts.values(), key=lambda a: a.timestamp, reverse=True)

    def upsert_incident(self, incident: Incident) -> Incident:
        self.incidents[incident.id] = incident
        return incident

    def list_incidents(self) -> list[Incident]:
        return sorted(self.incidents.values(), key=lambda i: i.created_at, reverse=True)


repo = InMemoryRepository()
