from datetime import datetime, timedelta


def correlate_failed_login_then_priv_esc(events: list[dict]) -> bool:
    failed = [
        e for e in events if e.get("event", {}).get("action") == "failed_login"
    ]
    priv = [
        e for e in events if e.get("event", {}).get("action") == "privilege_escalation"
    ]
    if len(failed) < 5 or not priv:
        return False

    first_failed = min(datetime.fromisoformat(e["@timestamp"]) for e in failed)
    first_priv = min(datetime.fromisoformat(e["@timestamp"]) for e in priv)
    return first_priv - first_failed <= timedelta(minutes=15)
