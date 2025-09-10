# src/observability.py
import os
import json
import time
from typing import Dict, Any
from datetime import datetime

ARTIFACTS_DIR = "artifacts"

def record_run_trace(run_id: str, trace: Dict[str, Any]):
    ts = datetime.utcnow().isoformat() + "Z"
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    filename = f"{ARTIFACTS_DIR}/run_{run_id}_{int(time.time())}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump({"run_id": run_id, "ts": ts, "trace": trace}, f, indent=2)
    return filename

def summarize_metrics(trace: Dict[str, Any]) -> Dict[str, Any]:
    # naive summarization of trace
    metrics = {
        "token_usage": trace.get("tokens", {}),
        "avg_tool_latency": None,
        "failure_counts": trace.get("failure_counts", {}),
        "fallback_rate": trace.get("fallback_rate", 0.0)
    }
    # compute average latency if tool latencies exist
    latencies = trace.get("tool_latencies", [])
    if latencies:
        metrics["avg_tool_latency"] = sum(latencies) / len(latencies)
    return metrics
