from enforcement.deterministic import enforce_deterministic
from enforcement.probabilistic import enforce_probabilistic

def hybrid_enforce(action: dict, context: dict):
    det = enforce_deterministic(action, context)
    if not det.get("allowed"):
        return det

    prob = enforce_probabilistic(action)
    if not prob.get("allowed"):
        return prob

    return {
        "allowed": True,
        "policy": "hybrid_v1",
        "risk_score": prob.get("risk_score", 0)
    }
