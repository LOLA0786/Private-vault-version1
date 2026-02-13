import os
from openai import OpenAI
from firewall_core_logic import enforce_logic
from decision_ledger import DecisionLedger

from drift_prompt import detect_prompt_drift
from drift_model import detect_model_drift
from drift_policy import detect_policy_drift

ledger = DecisionLedger()


def _get_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")
    return OpenAI(api_key=api_key, base_url="https://api.x.ai/v1")


def call_grok_and_enforce(prompt: str, principal: dict):

    client = _get_client()

    response = client.chat.completions.create(
        model="grok-4-0709",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    content = response.choices[0].message.content
    model_name = response.model

    # Drift detection (returns dicts)
    prompt_drift = detect_prompt_drift(prompt)
    model_drift = detect_model_drift(content)
    policy_drift = detect_policy_drift()

    # Extract numeric scores safely
    prompt_score = float(prompt_drift.get("drift_score", 0.0))
    model_score = float(model_drift.get("drift_score", 0.0))
    policy_score = float(policy_drift.get("drift_score", 0.0))

    combined_score = (prompt_score + model_score + policy_score) / 3.0

    action = {
        "tool": "llm_output",
        "content": content
    }

    decision = enforce_logic(
        action=action,
        principal=principal,
        context=action
    )

    # Unified ledger event AFTER full evaluation
    ledger.log_interaction("ai_firewall_event", {
        "model": model_name,
        "prompt_hash": hash(prompt),
        "response_hash": hash(content),
        "principal": principal.get("tenant_id"),
        "drift": {
            "prompt": prompt_drift,
            "model": model_drift,
            "policy": policy_drift,
            "combined_score": combined_score
        },
        "decision": decision
    })

    return {
        "drift": {
            "prompt": prompt_drift,
            "model": model_drift,
            "policy": policy_drift,
            "combined_score": combined_score
        },
        "llm_output": content,
        "firewall_decision": decision
    }
