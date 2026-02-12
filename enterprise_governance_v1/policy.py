import os
import json
import hashlib

def load_policy_bundle(path: str):
    if not os.path.exists(path):
        raise RuntimeError("POLICY_BUNDLE_NOT_FOUND")

    with open(path, "rb") as f:
        data = f.read()

    if not data:
        raise RuntimeError("POLICY_BUNDLE_EMPTY")

    # Placeholder for real signature validation
    digest = hashlib.sha256(data).hexdigest()

    print("Policy bundle loaded:", digest)
