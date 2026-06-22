#!/usr/bin/env python3
"""Generate 500 synthetic SIEM alerts."""

import json
import random
from pathlib import Path

import random
from pathlib import Path

random.seed(42)
DEMO_DIR = Path(__file__).resolve().parent.parent / "demo-data"
TYPES = ["brute_force", "malware", "phishing", "lateral_movement", "data_exfil"]
DESCRIPTIONS = [
    "Multiple failed authentication attempts detected.",
    "Suspicious outbound connection to rare destination.",
    "Encoded PowerShell execution observed.",
    "Possible data exfiltration over DNS.",
]


def _fake_ip() -> str:
    return f"203.0.{random.randint(1, 255)}.{random.randint(1, 254)}"


def main():
    DEMO_DIR.mkdir(parents=True, exist_ok=True)
    path = DEMO_DIR / "siem_alerts.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for i in range(1, 501):
            alert = {
                "id": f"ALERT-{i:04d}",
                "type": random.choice(TYPES),
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "source_ip": _fake_ip(),
                "hostname": f"srv-{random.randint(1, 50):02d}",
                "description": random.choice(DESCRIPTIONS),
                "mitre": random.choice(["T1110", "T1566", "T1021", "T1048"]),
            }
            f.write(json.dumps(alert) + "\n")
    print(f"Wrote 500 alerts to {path}")


if __name__ == "__main__":
    main()
