from typing import Dict, Any


HARD_LIMIT = 10000


def enforce(action: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deterministic enforcement BEFORE execution.
    """

    amount = float(action.get("amount", 0))

    if amount > HARD_LIMIT:
        return {
            "allowed": False,
            "reason": "Amount exceeds deterministic hard limit",
            "policy": "hard_limit_v1"
        }

    return {
        "allowed": True,
        "reason": "Within deterministic limits",
        "policy": "hard_limit_v1"
    }
