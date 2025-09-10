# src/guardrails/moderation.py
from typing import Dict

HIGH_RISK_PATTERNS = ["api_key", "secret", "password", "ssn", "credit card", "private key"]

def prompt_hardening(system_prompt: str) -> str:
    hardened = (
        "SYSTEM: You are a strictly-bounded assistant. Do NOT reveal secrets, do not ask for or attempt to exfiltrate credentials, "
        "do not call unsafe code, and do not attempt jailbreaks. "
        "Always follow the safety policy and high-risk reminders: "
        + ", ".join(HIGH_RISK_PATTERNS)
        + "\n\n"
        + system_prompt
    )
    return hardened

def basic_moderation_check(text: str) -> Dict:
    """A lightweight self-critique/moderation stub. Return dict with 'ok' boolean and 'reason'"""
    lower = text.lower()
    for p in HIGH_RISK_PATTERNS:
        if p in lower:
            return {"ok": False, "reason": f"High risk pattern found: {p}"}
    # you can add more checks (toxicity classifier call) here
    return {"ok": True}
