from policy_engine import authorize_intent
from drift_detection import DriftDetector
from decision_ledger import DecisionLedger

drift = DriftDetector(threshold=0.7)
ledger = DecisionLedger()

def enforce_logic(action: dict, principal: dict, context: dict | None = None):
    context = context or {}

    # -----------------------------
    # 1️⃣ Deterministic Enforcement
    # -----------------------------
    policy = authorize_intent(
        action,
        principal=principal,
        context=context
    )

    if not policy.get("allowed", False):
        ledger.log_interaction("deterministic_block", policy)
        return {
            "allowed": False,
            "layer": "deterministic",
            "reason": policy.get("reason")
        }

    # -----------------------------------
    # 2️⃣ Skip Drift for LLM Text Output
    # -----------------------------------
    if action.get("tool") == "llm_output":
        ledger.log_interaction("llm_response", action)
        return {
            "allowed": True,
            "layer": "llm_output",
            "note": "Non-executable content"
        }

    # -----------------------------
    # 3️⃣ Behavioral Drift Layer
    # -----------------------------
    drift_result = drift.detect_drift(
        prompt=str(action),
        actions=[action]
    )

    if drift_result.get("should_block"):
        ledger.log_interaction("drift_block", drift_result)
        return {
            "allowed": False,
            "layer": "behavioral",
            "reason": drift_result.get("reason")
        }

    # -----------------------------
    # 4️⃣ Approved Execution
    # -----------------------------
    ledger.log_interaction("approved", action)

    return {
        "allowed": True,
        "layer": "approved"
    }
