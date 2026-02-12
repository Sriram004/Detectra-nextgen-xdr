from typing import Any


def run_playbook(playbook: dict[str, Any], alert: dict[str, Any]) -> list[dict[str, Any]]:
    executed_steps: list[dict[str, Any]] = []
    for step in playbook.get("steps", []):
        params = {
            key: (value.replace("{{alert.host_id}}", alert.get("host_id", "")) if isinstance(value, str) else value)
            for key, value in step.get("params", {}).items()
        }
        executed_steps.append({
            "action": step.get("action"),
            "params": params,
            "status": "queued",
        })
    return executed_steps
