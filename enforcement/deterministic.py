def enforce_deterministic(action: dict, context: dict):
    amount = float(action.get("amount", 0))

    if amount > 10000:
        return {
            "allowed": False,
            "reason": "Amount exceeds deterministic hard limit",
            "policy": "hard_limit_v2"
        }

    return {"allowed": True}
