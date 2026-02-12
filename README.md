# Detectra NextGen XDR (MVP Scaffold)

A starter implementation of a Cortex XDR–style platform with:
- telemetry ingestion endpoint
- Sigma-style rule matching
- basic incident correlation
- SOAR playbook execution API
- JWT-like role gate for response actions

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
uvicorn apps.api.app.main:app --reload
```

OpenAPI: `http://127.0.0.1:8000/docs`

## API endpoints
- `GET /healthz`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/seed`
- `POST /api/v1/alerts/ingest`
- `GET /api/v1/incidents`
- `POST /api/v1/playbooks/run` (requires role `admin` or `responder`)

## Auth format (MVP)
`Authorization: Bearer username:role`

Examples:
- `Bearer alice:analyst`
- `Bearer bob:responder`

## Included rules
- Sigma: `rules/sigma/suspicious_powershell_encoded.yml`
- Correlation: `rules/correlation/failed_login_then_priv_esc.yml`
- Playbook: `rules/playbooks/contain_suspicious_powershell.yml`
