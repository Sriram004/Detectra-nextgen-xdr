from typing import Any


def _resolve_path(event: dict[str, Any], dotted: str) -> Any:
    value: Any = event
    for part in dotted.split("."):
        if isinstance(value, dict):
            value = value.get(part)
        else:
            return None
    return value


def _match_operator(field_value: Any, op: str, expected: Any) -> bool:
    text = str(field_value or "")
    if op == "endswith":
        return text.lower().endswith(str(expected).lower())
    if op == "contains":
        if isinstance(expected, list):
            return any(item.lower() in text.lower() for item in expected)
        return str(expected).lower() in text.lower()
    if op == "equals":
        return str(field_value) == str(expected)
    return False


def match_sigma_rule(rule: dict[str, Any], event: dict[str, Any]) -> bool:
    detection = rule.get("detection", {})
    checks = []

    for section, predicates in detection.items():
        if section == "condition":
            continue
        section_result = True
        for key, expected in predicates.items():
            if "|" in key:
                field, op = key.split("|", 1)
            else:
                field, op = key, "equals"
            field_value = _resolve_path(event, field)
            section_result = section_result and _match_operator(field_value, op, expected)
        checks.append((section, section_result))

    condition = detection.get("condition", " and ".join(name for name, _ in checks))
    truth_map = {name: result for name, result in checks}

    # Minimal evaluator supporting "and" and "or" tokens between section names
    tokens = condition.split()
    if not tokens:
        return False

    result = truth_map.get(tokens[0], False)
    idx = 1
    while idx < len(tokens) - 1:
        operator = tokens[idx].lower()
        rhs = truth_map.get(tokens[idx + 1], False)
        if operator == "and":
            result = result and rhs
        elif operator == "or":
            result = result or rhs
        idx += 2
    return result
