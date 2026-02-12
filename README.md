# Detectra NextGen XDR

> A modular, FastAPI-based MVP for building a Cortex XDR–like platform (ingest → detect → correlate → respond).

## Table of Contents
- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Detection & Playbook Examples](#detection--playbook-examples)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [License](#license)

## Overview
Detectra NextGen XDR is a starter platform for Extended Detection and Response workflows:
- ingest security telemetry
- normalize and evaluate detections
- create/merge incidents
- run SOAR-style response playbooks

This repository is intentionally MVP-first and favors clarity/extensibility over production completeness.

## Architecture
Current MVP flow:
1. Event payload is posted to `/api/v1/alerts/ingest`.
2. Sigma-style rules are loaded from `rules/sigma/`.
3. Matched events produce alerts.
4. Alerts are grouped into incidents using simple host-based merge logic.
5. Responders/admins can run playbooks through `/api/v1/playbooks/run`.

See `XDR_PLATFORM_BLUEPRINT.md` for the full target architecture and expansion plan.

## Features
- FastAPI app with modular routes (`alerts`, `incidents`, `playbooks`)
- In-memory repository for alerts/incidents (MVP storage)
- Sigma-style rule loader + evaluator (`endswith`, `contains`, `equals`)
- Correlation helper (failed login burst + privilege escalation sequence)
- UEBA helper (z-score baseline anomaly check)
- SOAR playbook runner with simple alert parameter templating
- Lightweight role enforcement on playbook execution

## Project Structure
```text
apps/api/app/
  auth/            # auth dependencies + role checks
  core/            # settings/config
  db/              # in-memory repository
  routes/          # API route modules
  schemas/         # Pydantic models
  services/        # alert/incident workflows
services/
  detection/       # rule engine, correlation, UEBA helpers
  response_engine/ # playbook execution
rules/
  sigma/           # Sigma-like detection rules
  correlation/     # correlation rule definitions
  playbooks/       # SOAR playbooks
tests/             # unit/integration-style tests
```

## Getting Started
### 1) Create environment
```bash
python -m venv .venv
source .venv/bin/activate
```

### 2) Install dependencies
```bash
pip install -e .[dev]
```

### 3) Run API
```bash
uvicorn apps.api.app.main:app --reload
```

OpenAPI docs: `http://127.0.0.1:8000/docs`

## Configuration
Configuration is currently centralized in `apps/api/app/core/config.py`.

Planned next step: move to environment-driven settings (e.g., `.env`) for secret and environment management.

## API Reference
- `GET /healthz`
- `GET /api/v1/alerts`
- `POST /api/v1/alerts/seed`
- `POST /api/v1/alerts/ingest`
- `GET /api/v1/incidents`
- `POST /api/v1/playbooks/run`

### MVP Auth Header Format
For role simulation, pass:
```text
Authorization: Bearer <username>:<role>
```
Examples:
- `Bearer alice:analyst`
- `Bearer bob:responder`
- `Bearer root:admin`

## Detection & Playbook Examples
- Sigma rule: `rules/sigma/suspicious_powershell_encoded.yml`
- Correlation rule: `rules/correlation/failed_login_then_priv_esc.yml`
- Playbook: `rules/playbooks/contain_suspicious_powershell.yml`

## Testing
```bash
python -m pytest -q
```

If dependencies are unavailable in your environment, you can still verify syntax with:
```bash
python -m compileall apps services tests
```

## Roadmap
- Replace in-memory repository with PostgreSQL + OpenSearch
- Add Kafka/RabbitMQ ingestion workers
- Add ClickHouse analytics pipelines
- Add Celery-based distributed playbook execution
- Add robust JWT/OIDC auth and fine-grained RBAC
- Add ATT&CK mapping + threat intel enrichment

## Contributing
1. Fork and create a feature branch.
2. Add tests for changes.
3. Open a pull request with validation notes.

## License
Internal/proprietary by default unless replaced with a project license.
