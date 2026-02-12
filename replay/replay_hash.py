import hashlib
import json


def compute_replay_hash(payload: dict) -> str:
    serialized = json.dumps(payload, sort_keys=True).encode()
    return hashlib.sha256(serialized).hexdigest()
