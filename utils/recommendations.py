import yaml
from pathlib import Path

def load_recommendations(config_path: str):
    with open(config_path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg.get("recommendations", {}), float(cfg.get("risk_threshold", 0.7))

def suggest(playbook: dict, record: dict):
    recos = list(playbook.get("default", []))
    et = (record.get("event_type") or "").lower()
    if "brute" in et or (record.get("auth_failures",0) or 0) > 3:
        recos = recos + playbook.get("auth_failure", [])
    if "malware" in et or (record.get("malware_alerts",0) or 0) > 0:
        recos = recos + playbook.get("malware", [])
    # de-duplicate while preserving order
    seen = set()
    dedup = []
    for r in recos:
        if r not in seen:
            seen.add(r)
            dedup.append(r)
    return dedup
