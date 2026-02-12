from fastapi.testclient import TestClient
from apps.api.app.main import app


def test_healthz() -> None:
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_ingest_creates_alert() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/alerts/ingest",
        json={
            "payload": {
                "host": {"id": "host-99"},
                "process": {
                    "name": "powershell.exe",
                    "command_line": "powershell.exe -EncodedCommand AAAA",
                },
            }
        },
    )
    assert response.status_code == 200
    assert response.json()["alerts_created"] >= 1
