from src.agents.runner import run_agent

def test_supervisor_triage():
    out = run_agent("Investigate ALERT-0001")
    assert out["answer"]
    assert any("TriageAgent" in str(t) for t in out["trace"])
