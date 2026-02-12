"""
PrivateVault Deterministic Policy Engine v3
Hard pre-execution enforcement.
Versioned. Deterministic. No fallback ambiguity.
"""

POLICY_VERSION = "v3_deterministic"

HARD_TRANSFER_LIMIT = 10000


def authorize_intent(action: dict, principal: dict = None, context: dict = None):
    principal = principal or {}
    context = context or {}

    tool = action.get("tool")
    amount = float(context.get("amount", 0))

    if tool == "transfer_funds" and amount > HARD_TRANSFER_LIMIT:
        return {
            "allowed": False,
            "policy_version": POLICY_VERSION,
            "reason": "Amount exceeds deterministic hard limit"
        }

    return {
        "allowed": True,
        "policy_version": POLICY_VERSION,
        "reason": "Allowed under deterministic policy"
    }
