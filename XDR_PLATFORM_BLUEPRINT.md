# Cortex XDR–Like Platform Blueprint

## 1) System Architecture

```text
Telemetry Sources
  ├─ Endpoints: Winlogbeat, Osquery, Sysmon, EDR agent
  ├─ Network: Zeek, Suricata, Firewall logs, DNS logs
  └─ Cloud: AWS CloudTrail, GuardDuty, VPC Flow Logs
        │
        ▼
[Ingestion Adapters / Collectors]
  - Beats/Fluent Bit/Vector collectors
  - API pullers (CloudTrail, SaaS APIs)
  - Broker producers
        │
        ▼
[Message Bus]
  Kafka (preferred) topics by source + schema version
  or RabbitMQ exchanges/queues
        │
        ▼
[Normalization & Enrichment Pipeline]
  - Parse raw events
  - Map to ECS-like schema
  - Enrich with GeoIP, asset inventory, identity context, threat intel
        │
        ├──────────────────────────────┐
        ▼                              ▼
[Hot Search Storage]               [Analytics Warehouse]
  OpenSearch/ElasticSearch         ClickHouse
  (fast triage/search)             (long-term analytics, aggregations)
        │                              │
        └──────────────┬───────────────┘
                       ▼
               [Detection Engine]
        - Rule engine (Sigma-style YAML)
        - Correlation engine (multi-event sequences)
        - UEBA anomaly detector (baseline + z-score/isolation forest)
                       │
                       ▼
       [Alert Service & Incident Correlation]
        - Deduplicate and merge alerts
        - Severity scoring + priority
        - Incident timeline graph
        - Persist alerts/incidents (PostgreSQL + OpenSearch index)
                       │
         ┌─────────────┴──────────────┐
         ▼                            ▼
 [SOAR / Response Engine]         [Web/API Layer]
  Celery workers + playbooks       FastAPI + WebSockets
  - isolate endpoint               React + Tailwind dashboard
  - disable user                   - alert queue
  - block IP                       - incident timeline
                                   - host/user detail pages
```

---

## 2) Recommended Tech Stack

### Backend / Platform
- **Core API:** FastAPI (Python)
- **Async tasks / SOAR:** Celery + Redis/RabbitMQ broker
- **Streaming:** Kafka (high-throughput, replay, partitioning)
- **Schema/validation:** Pydantic models
- **Rule parsing:** PyYAML + custom Sigma-compatible evaluator
- **ML/UEBA:** scikit-learn (IsolationForest, OneClassSVM), river (streaming)
- **Auth/security:** JWT (PyJWT), RBAC middleware, bcrypt/argon2

### Data Stores
- **OpenSearch/ElasticSearch:** hot searchable telemetry + alert index
- **ClickHouse:** long-term analytical queries and dashboards
- **PostgreSQL:** users, RBAC, incidents, workflow state, audit trail
- **Redis:** cache, rate limiting, session blacklist, Celery backend

### Frontend
- **Framework:** React + TypeScript + Vite
- **Styling:** Tailwind CSS
- **State/data:** React Query + Zustand/Redux Toolkit
- **Realtime:** WebSocket/SSE for live alerts and incident updates
- **Charts:** ECharts or Recharts

### Ops / Infra
- **Containerization:** Docker + Docker Compose (dev), Kubernetes (prod)
- **IaC:** Terraform + Helm
- **Observability:** Prometheus + Grafana + Loki/ELK logs
- **CI/CD:** GitHub Actions/GitLab CI

---

## 3) Modular Project Folder Structure

```text
xdr-platform/
├── apps/
│   ├── api/                               # FastAPI app
│   │   ├── app/
│   │   │   ├── main.py
│   │   │   ├── core/                      # config, logging, security
│   │   │   ├── auth/                      # JWT, RBAC, user mgmt
│   │   │   ├── routes/                    # alerts, incidents, hosts, playbooks
│   │   │   ├── services/
│   │   │   │   ├── incident_service.py
│   │   │   │   ├── alert_service.py
│   │   │   │   └── search_service.py
│   │   │   ├── db/                        # pg models + migrations + repos
│   │   │   └── websocket/                 # realtime event push
│   │   └── tests/
│   └── web/                               # React + Tailwind
│       ├── src/
│       │   ├── pages/
│       │   │   ├── AlertQueue.tsx
│       │   │   ├── IncidentTimeline.tsx
│       │   │   ├── HostDetails.tsx
│       │   │   └── PlaybookRunner.tsx
│       │   ├── components/
│       │   ├── features/
│       │   ├── api/
│       │   ├── hooks/
│       │   └── store/
│       └── tests/
├── services/
│   ├── ingestion/
│   │   ├── collectors/                    # osquery, zeek, cloudtrail adapters
│   │   ├── kafka_producers/
│   │   └── parsers/
│   ├── normalization/
│   │   ├── ecs_mapper/
│   │   ├── enrichers/                     # geoip, asset, identity, threat intel
│   │   └── schemas/
│   ├── detection/
│   │   ├── rule_engine/
│   │   │   ├── sigma_loader.py
│   │   │   ├── evaluator.py
│   │   │   └── rules/
│   │   ├── correlation_engine/
│   │   └── ueba/
│   ├── incident_correlation/
│   │   ├── merger.py
│   │   ├── scorer.py
│   │   └── dedup.py
│   └── response_engine/
│       ├── celery_app.py
│       ├── playbook_runner.py
│       └── actions/
│           ├── disable_user.py
│           ├── block_ip.py
│           └── isolate_endpoint.py
├── rules/
│   ├── sigma/
│   ├── correlation/
│   └── suppression/
├── data-model/
│   ├── ecs_like_schema.json
│   ├── index_templates/
│   └── clickhouse/
├── deployments/
│   ├── docker-compose.yml
│   ├── helm/
│   └── terraform/
├── docs/
│   ├── architecture.md
│   ├── api-spec.yaml
│   ├── runbooks/
│   └── threat-model.md
└── scripts/
    ├── seed_rules.py
    ├── replay_events.py
    └── benchmark_pipeline.py
```

---

## 4) Data Model (ECS-like Normalized Event)

```json
{
  "@timestamp": "2026-02-12T10:15:00Z",
  "event": {
    "id": "evt-123",
    "kind": "event",
    "category": ["process"],
    "type": ["start"],
    "dataset": "osquery.process_events",
    "severity": 4
  },
  "host": {
    "id": "host-01",
    "name": "finance-laptop-01",
    "ip": ["10.10.5.24"],
    "os": { "name": "Windows", "version": "11" }
  },
  "user": {
    "id": "u-445",
    "name": "j.doe",
    "domain": "CORP"
  },
  "process": {
    "pid": 4420,
    "name": "powershell.exe",
    "command_line": "powershell.exe -enc SQBtA...",
    "parent": { "name": "winword.exe", "pid": 981 }
  },
  "network": {
    "direction": "outbound"
  },
  "cloud": {
    "provider": "aws",
    "account": { "id": "123456789012" },
    "region": "us-east-1"
  },
  "xdr": {
    "source": "osquery",
    "tenant": "acme",
    "ingest_pipeline": "v1"
  }
}
```

---

## 5) Detection Engine Design

### Rule-based Detection (Sigma-style)
1. Load YAML rules from `rules/sigma/`.
2. Compile conditions into executable predicates.
3. Match normalized events in stream/batch.
4. Emit alerts with metadata: `rule_id`, `confidence`, `severity`, `tactics`, `techniques`.

### Correlation Rules
- Use sliding windows and entity keys (`host.id`, `user.id`, `src.ip`).
- Example: `failed logins >= 5 in 10m` followed by `privilege change` within 15m.
- Persist intermediate state in Redis/ClickHouse materialized views.

### ML UEBA (Simple Version)
- Feature examples per user/host/hour:
  - failed logins
  - distinct destination IPs
  - off-hours activity score
  - process entropy / rare process score
- Train per-entity baseline model and detect anomaly score threshold exceedance.
- Use model outputs as **supporting signal**, not sole decision.

---

## 6) FastAPI Backend Example Snippets

### A) Alert model + API route

```python
# apps/api/app/routes/alerts.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/alerts", tags=["alerts"])

class AlertOut(BaseModel):
    id: str
    rule_id: str
    severity: str
    status: str
    host_id: str
    timestamp: str

@router.get("", response_model=List[AlertOut])
async def list_alerts(limit: int = 50):
    # Replace with repository search from OpenSearch/Postgres
    return [
        AlertOut(
            id="a-1001",
            rule_id="suspicious_powershell_encoded",
            severity="high",
            status="new",
            host_id="host-01",
            timestamp="2026-02-12T10:15:00Z",
        )
    ]
```

### B) JWT + RBAC dependency

```python
# apps/api/app/auth/deps.py
from fastapi import Depends, HTTPException


def require_role(allowed_roles: set[str]):
    def checker(current_user=Depends(get_current_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Forbidden")
        return current_user
    return checker

# Usage in route
# @router.post("/playbooks/{id}/run", dependencies=[Depends(require_role({"admin", "responder"}))])
```

---

## 7) React + Tailwind Frontend Example Snippet

```tsx
// apps/web/src/pages/AlertQueue.tsx
import { useEffect, useState } from "react";

type Alert = {
  id: string;
  rule_id: string;
  severity: "low" | "medium" | "high" | "critical";
  status: string;
  host_id: string;
  timestamp: string;
};

export default function AlertQueue() {
  const [alerts, setAlerts] = useState<Alert[]>([]);

  useEffect(() => {
    fetch("/api/alerts")
      .then((r) => r.json())
      .then(setAlerts);
  }, []);

  return (
    <div className="p-4">
      <h1 className="text-xl font-semibold mb-4">Alert Queue</h1>
      <div className="space-y-2">
        {alerts.map((a) => (
          <div key={a.id} className="border rounded p-3 bg-white shadow-sm">
            <div className="flex justify-between">
              <span className="font-mono text-sm">{a.rule_id}</span>
              <span className="text-red-600 font-medium">{a.severity}</span>
            </div>
            <p className="text-sm text-gray-600">Host: {a.host_id}</p>
            <p className="text-xs text-gray-500">{a.timestamp}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
```

---

## 8) Sigma-style Detection Rule Example

```yaml
title: Suspicious PowerShell Encoded Command
id: 8e5c4ef6-1a2b-4e6d-b2aa-7f9df6edb001
status: experimental
description: Detects PowerShell execution with encoded command flags often used in malware.
author: SOC Team
date: 2026-02-12
logsource:
  product: windows
  category: process_creation
detection:
  selection_img:
    process.name|endswith: "powershell.exe"
  selection_cmd:
    process.command_line|contains:
      - " -enc "
      - " -EncodedCommand "
      - "FromBase64String"
  condition: selection_img and selection_cmd
falsepositives:
  - Legitimate admin scripts using encoded commands
level: high
tags:
  - attack.execution
  - attack.t1059.001
```

---

## 9) Incident Correlation & Alert Management Logic

- **Dedup key:** `rule_id + host.id + user.id + time_bucket(5m)`
- **Incident grouping:** graph-based clustering on shared entities (`host`, `user`, `ip`, `hash`)
- **Priority formula:**
  - `priority = severity_weight + asset_criticality + confidence + threat_intel_score`
- **Lifecycle:** `new -> triaged -> investigating -> contained -> resolved -> closed`
- **Storage pattern:**
  - Alerts: OpenSearch index + Postgres metadata
  - Incidents: Postgres relational core + OpenSearch timeline index

---

## 10) SOAR / Response Engine

### Playbook YAML Example

```yaml
name: Contain Suspicious PowerShell Host
trigger:
  rule_id: suspicious_powershell_encoded
steps:
  - action: isolate_endpoint
    params:
      host_id: "{{alert.host_id}}"
  - action: block_ip
    params:
      ip: "{{alert.destination_ip}}"
  - action: create_ticket
    params:
      system: jira
      project: SEC
```

### Execution Model
- Trigger from alert conditions or analyst click.
- Execute asynchronously via Celery workers.
- Every step writes audit events to PostgreSQL.
- Include rollback and approval gates for high-risk actions.

---

## 11) Security & RBAC

- JWT access + refresh tokens.
- Roles:
  - **admin:** platform config, users, connectors, all playbooks
  - **analyst:** read/search telemetry, triage alerts, open incidents
  - **responder:** run containment playbooks, update incident status
- Mandatory controls:
  - MFA for admin accounts
  - signed and encrypted agent-to-ingestion traffic (mTLS)
  - full audit logs for analyst queries and response actions
  - field-level controls for sensitive data (PII masking)

---

## 12) Analytics Dashboards (ClickHouse + OpenSearch)

- Event ingest volume by source / tenant / hour
- Detection hit rate by rule (precision trend)
- Mean time to detect (MTTD), mean time to respond (MTTR)
- Top attacked hosts/users
- False positive ratio by rule and analyst feedback
- Playbook success/failure and median execution time

---

## 13) Future Extensions

1. **Threat Intel (MISP):**
   - Pull IOCs into enrichment layer.
   - Match IOC hits during normalization and correlation.
2. **MITRE ATT&CK Mapping:**
   - Tag all rules and incidents with tactics/techniques.
   - Build ATT&CK heatmap in UI.
3. **Sandbox Integration:**
   - Auto-submit suspicious files/URLs to sandbox.
   - Ingest verdict as enrichment to raise/lower confidence.
4. **Advanced Graph Correlation:**
   - Neo4j/OpenSearch graph exploration for lateral movement paths.
5. **ModelOps for UEBA:**
   - Drift detection, scheduled retraining, shadow model rollout.

---

## 14) Suggested Build Phases

- **Phase 1 (MVP):** ingestion + normalization + rule engine + alert queue
- **Phase 2:** incidents, correlation, RBAC, playbook execution
- **Phase 3:** UEBA anomalies, ATT&CK mapping, analytics dashboards
- **Phase 4:** threat intel + sandbox + multi-tenant hardening

