import hashlib
import json
import os

LAST_POLICY_HASH = None

def _hash_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def detect_policy_drift(policy_path="policy_bundle.json"):
    global LAST_POLICY_HASH

    if not os.path.exists(policy_path):
        return {"drift_score": 1.0, "reason": "policy_missing"}

    current_hash = _hash_file(policy_path)

    if LAST_POLICY_HASH is None:
        LAST_POLICY_HASH = current_hash
        return {"drift_score": 0.0}

    if current_hash != LAST_POLICY_HASH:
        drift = 1.0
    else:
        drift = 0.0

    LAST_POLICY_HASH = current_hash

    return {
        "drift_score": drift,
        "current_hash": current_hash
    }
