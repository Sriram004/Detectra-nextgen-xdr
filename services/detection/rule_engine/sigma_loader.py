from pathlib import Path
import yaml


class SigmaLoader:
    def __init__(self, rules_dir: str = "rules/sigma") -> None:
        self.rules_dir = Path(rules_dir)

    def load_all(self) -> list[dict]:
        rules: list[dict] = []
        for path in sorted(self.rules_dir.glob("*.yml")) + sorted(self.rules_dir.glob("*.yaml")):
            with path.open("r", encoding="utf-8") as handle:
                rules.append(yaml.safe_load(handle))
        return rules
