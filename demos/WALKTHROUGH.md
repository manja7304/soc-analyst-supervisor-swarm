# Demo Walkthrough — SOC Analyst Supervisor Swarm

**Pattern:** LangGraph Supervisor  
**Captured:** 2026-06-24 with `USE_MOCK_LLM=true` (no Docker/Ollama required)

---

## Prerequisites

```bash
cp .env.example .env   # optional for mock demo
pip install -r requirements.txt
```

---

## Step 1 — One-command demo

```bash
export USE_MOCK_LLM=true
python scripts/run_demo.py
```

This runs the same FastAPI `TestClient` path as CI — real code, real JSON output.

### Step 2 — Agent API call

```bash
curl -X POST http://localhost:8080/api/v1/agent/run \
  -H "Content-Type: application/json" \
  -d '{"query": "Investigate ALERT-0042"}'
```

Or offline (no server):

```bash
USE_MOCK_LLM=true python scripts/run_demo.py
```

**Request (`demos/captured/request.json`):**

```json
{
  "query": "Investigate ALERT-0042"
}
```

**Response (`demos/captured/response.json`):**

```json
{
  "answer": "Triage complete for ALERT-0042",
  "trace": [
    {
      "agent": "TriageAgent",
      "output": {
        "id": "ALERT-0042",
        "type": "data_exfil",
        "severity": "low",
        "source_ip": "203.0.192.81",
        "hostname": "srv-04",
        "description": "Multiple failed authentication attempts detected.",
        "mitre": "T1048"
      }
    }
  ],
  "metadata": {}
}
```

### Step 3 — Agent trace excerpt

```json
[
  {
    "agent": "TriageAgent",
    "output": {
      "id": "ALERT-0042",
      "type": "data_exfil",
      "severity": "low",
      "source_ip": "203.0.192.81",
      "hostname": "srv-04",
      "description": "Multiple failed authentication attempts detected.",
      "mitre": "T1048"
    }
  }
]
```

---

## Architecture callout (2-min video)

> LangGraph supervisor with keyword routing to Triage/ThreatIntel/Forensics/Report specialists over 500 SIEM alerts — zero LLM routing cost.

Highlight in your recording:

1. **Problem → pattern** — why this agent architecture fits the security domain
2. **Tool/trace output** — show structured JSON, not just the final answer
3. **`docs/architecture.md`** — Mermaid diagram for the close

---

## Artifacts

| File | Description |
|------|-------------|
| [`demos/captured/request.json`](captured/request.json) | API request payload |
| [`demos/captured/response.json`](captured/response.json) | Live captured response |
| [`demos/captured/trace.json`](captured/trace.json) | Agent trace array |
| [`demos/captured/terminal-session.txt`](captured/terminal-session.txt) | Terminal replay for Loom |

---

## Record your video

```bash
python scripts/run_demo.py
```

Use [`demos/RECORDING_SCRIPT.md`](RECORDING_SCRIPT.md) for shot list and narration cues.
