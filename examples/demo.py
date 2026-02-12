from enforcement.engine import enforce
from ledger.decision_ledger import DecisionLedger
from replay.replay_hash import compute_replay_hash


ledger = DecisionLedger()

action = {
    "tool": "transfer_funds",
    "amount": 50000
}

# Deterministic enforcement
decision = enforce(action)

# Log decision
ledger.log("policy_decision", {
    "action": action,
    "decision": decision
})

# Compute replay hash
replay_hash = compute_replay_hash({
    "action": action,
    "decision": decision
})

print("Decision:", decision)
print("Replay Hash:", replay_hash)
print("Ledger Valid:", ledger.verify())
