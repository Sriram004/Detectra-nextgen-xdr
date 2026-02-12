from services.detection.rule_engine.evaluator import match_sigma_rule


def test_sigma_rule_match_for_encoded_powershell() -> None:
    rule = {
        "detection": {
            "selection_img": {"process.name|endswith": "powershell.exe"},
            "selection_cmd": {"process.command_line|contains": [" -enc ", " -EncodedCommand "]},
            "condition": "selection_img and selection_cmd",
        }
    }
    event = {
        "process": {
            "name": "powershell.exe",
            "command_line": "powershell.exe -enc SGVsbG8=",
        }
    }
    assert match_sigma_rule(rule, event)
