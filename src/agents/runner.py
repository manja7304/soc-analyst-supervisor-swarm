"""LangGraph supervisor routing to specialist agents."""

from __future__ import annotations

import json

from langgraph.graph import END, StateGraph
from typing_extensions import TypedDict

from src.tools.soc_tools import fetch_alert, enrich_ioc, query_logs, generate_report


class State(TypedDict):
    query: str
    alert_type: str
    trace: list[dict]
    answer: str


def classify(state: State) -> State:
    q = state["query"].lower()
    if "malware" in q or "hash" in q:
        at = "threat_intel"
    elif "log" in q or "forensic" in q:
        at = "forensics"
    elif "report" in q:
        at = "report"
    else:
        at = "triage"
    return {**state, "alert_type": at}


def triage_agent(state: State) -> State:
    trace = list(state.get("trace", []))
    aid = state["query"].split()[-1] if "ALERT" in state["query"].upper() else "ALERT-0001"
    out = json.loads(fetch_alert.invoke(aid))
    trace.append({"agent": "TriageAgent", "output": out})
    return {**state, "trace": trace, "answer": f"Triage complete for {aid}"}


def threat_intel_agent(state: State) -> State:
    trace = list(state.get("trace", []))
    out = json.loads(enrich_ioc.invoke("192.0.2.1"))
    trace.append({"agent": "ThreatIntelAgent", "output": out})
    return {**state, "trace": trace, "answer": "Threat intel enrichment complete"}


def forensics_agent(state: State) -> State:
    trace = list(state.get("trace", []))
    out = json.loads(query_logs.invoke("srv-demo-01"))
    trace.append({"agent": "ForensicsAgent", "output": out})
    return {**state, "trace": trace, "answer": "Forensics log review complete"}


def report_agent(state: State) -> State:
    trace = list(state.get("trace", []))
    out = json.loads(generate_report.invoke("ALERT-0001", "Suspicious auth pattern"))
    trace.append({"agent": "ReportAgent", "output": out})
    return {**state, "trace": trace, "answer": "Report generated"}


def route(state: State) -> str:
    return state["alert_type"]


def build_graph():
    g = StateGraph(State)
    g.add_node("classify", classify)
    g.add_node("triage", triage_agent)
    g.add_node("threat_intel", threat_intel_agent)
    g.add_node("forensics", forensics_agent)
    g.add_node("report", report_agent)
    g.set_entry_point("classify")
    g.add_conditional_edges("classify", route, {
        "triage": "triage",
        "threat_intel": "threat_intel",
        "forensics": "forensics",
        "report": "report",
    })
    for n in ["triage", "threat_intel", "forensics", "report"]:
        g.add_edge(n, END)
    return g.compile()


def run_agent(query: str, context: dict | None = None) -> dict:
    state = build_graph().invoke({"query": query, "trace": [], "answer": "", "alert_type": ""})
    return {"answer": state["answer"], "trace": state["trace"], "metadata": context or {}}
