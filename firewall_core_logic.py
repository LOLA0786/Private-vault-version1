import os
from policy_engine import authorize_intent
from drift_detection import DriftDetector
from decision_ledger import DecisionLedger

def get_firewall_mode():
    import os
    return os.getenv("get_firewall_mode()", "hybrid")

drift = DriftDetector(threshold=0.7)
ledger = DecisionLedger()

def compute_risk(policy_result, drift_result):
    risk = 0.0

    if not policy_result.get("allowed", True):
        risk += 0.8

    if drift_result.get("should_block"):
        risk += 0.5

    return round(min(risk, 1.0), 3)

def enforce_logic(action: dict, principal: dict, context: dict | None = None):
    drift_score = context.get("drift_score", 0.0)

    context = context or {}
    tenant_id = principal.get("tenant_id", "default")

    # 1️⃣ Deterministic Enforcement
    policy = authorize_intent(action, principal=principal, context=context)

    if not policy.get("allowed"):
        ledger.log_interaction("deterministic_block", {
            "tenant": tenant_id,
            "policy": policy
        })

        return {
            "allowed": False,
            "layer": "deterministic",
            "reason": policy.get("reason"),
            "tenant": tenant_id,
            "mode": get_firewall_mode()
        }

    # 2️⃣ Behavioral Drift
    drift_result = drift.detect_drift(
        prompt=str(action),
        actions=[action]
    )

    risk_score = compute_risk(policy, drift_result)
    drift_score = context.get("drift_score", 0.0)
    if context.get("drift_score", 0.0) > 0.8:
        risk_score = 0.95
    drift_score = context.get("drift_score", 0.0)


    if get_firewall_mode() == "strict" and drift_result.get("should_block"):
        ledger.log_interaction("behavioral_block", {
            "tenant": tenant_id,
            "drift": drift_result
        })

        return {
            "allowed": False,
            "layer": "behavioral",
            "reason": drift_result.get("reason"),
            "risk_score": risk_score,
            "tenant": tenant_id,
            "mode": get_firewall_mode()
        }

    if get_firewall_mode() == "hybrid" and risk_score > 0.7:
        ledger.log_interaction("hybrid_block", {
            "tenant": tenant_id,
            "risk_score": risk_score
        })

        return {
            "allowed": False,
            "layer": "risk_threshold",
            "risk_score": risk_score,
            "tenant": tenant_id,
            "mode": get_firewall_mode()
        }

    # 3️⃣ Approved
    ledger.log_interaction("approved", {
        "tenant": tenant_id,
        "action": action,
        "risk_score": risk_score
    })

    return {
        "allowed": True,
        "layer": "approved",
        "risk_score": risk_score,
        "tenant": tenant_id,
        "mode": get_firewall_mode()
    }
