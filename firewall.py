from core.policy_engine import authorize_intent
from core.drift_detection import DriftDetector
from decision_ledger import DecisionLedger
from replay.replay_hash import compute_replay_hash

drift = DriftDetector(threshold=0.70)
ledger = DecisionLedger()


def enforce(action, principal=None, context=None):
    if principal is None:
        principal = {"role": "system"}

    context = context or {}

    # 1️⃣ Deterministic Gate
    policy_result = authorize_intent(action, principal=principal, context=context)
    if not policy_result["allowed"]:
        ledger.log_interaction("deterministic_block", policy_result)
        return {
            "allowed": False,
            "layer": "deterministic",
            "reason": policy_result["reason"]
        }

    # 2️⃣ Drift Detection
    drift_result = drift.detect(
        prompt=str(action),
        actions=[action]
    )

    if drift_result["should_block"]:
        ledger.log_interaction("drift_block", drift_result)
        return {
            "allowed": False,
            "layer": "drift",
            "reason": drift_result.get("reason", "drift threshold exceeded")
        }

    # 3️⃣ Replay Hash
    replay_hash = compute_replay_hash(action)

    ledger.log_interaction("approved", {
        "action": action,
        "replay_hash": replay_hash
    })

    return {
        "allowed": True,
        "layer": "approved",
        "replay_hash": replay_hash,
        "ledger_valid": ledger.verify_chain_integrity()
    }
