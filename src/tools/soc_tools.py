"""SOC investigation tools."""

from __future__ import annotations

import json
from pathlib import Path

from langchain_core.tools import tool

DEMO_DIR = Path(__file__).resolve().parent.parent.parent / "demo-data"


def _load_alerts() -> list[dict]:
    alerts = []
    path = DEMO_DIR / "siem_alerts.jsonl"
    for line in path.read_text(encoding="utf-8").strip().splitlines():
        if line.strip():
            alerts.append(json.loads(line))
    return alerts


@tool
def fetch_alert(alert_id: str) -> str:
    """Fetch a SIEM alert by id."""
    for a in _load_alerts():
        if a["id"] == alert_id:
            return json.dumps(a, indent=2)
    return json.dumps({"error": "not found"})


@tool
def enrich_ioc(ioc: str) -> str:
    """Enrich IOC with synthetic threat intel."""
    return json.dumps({
        "ioc": ioc,
        "reputation": "suspicious",
        "confidence": 0.82,
        "related_campaigns": ["APT-DEMO-1"],
    })


@tool
def query_logs(hostname: str) -> str:
    """Return synthetic log excerpts for a host."""
    return json.dumps({
        "hostname": hostname,
        "events": [
            {"ts": "2025-06-01T10:00:00Z", "event": "failed_login", "count": 42},
            {"ts": "2025-06-01T10:05:00Z", "event": "powershell_encoded", "count": 3},
        ],
    })


@tool
def generate_report(alert_id: str, findings: str) -> str:
    """Generate investigation report stub."""
    return json.dumps({
        "alert_id": alert_id,
        "status": "investigated",
        "findings": findings,
        "mitre": ["T1110", "T1059"],
    })
