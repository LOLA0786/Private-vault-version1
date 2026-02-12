import os
import json
import hashlib

def load_registry_bundle(path: str):
    if not os.path.exists(path):
        raise RuntimeError("REGISTRY_BUNDLE_NOT_FOUND")

    with open(path, "rb") as f:
        data = f.read()

    if not data:
        raise RuntimeError("REGISTRY_BUNDLE_EMPTY")

    # Placeholder for real signature validation
    digest = hashlib.sha256(data).hexdigest()

    print("Registry bundle loaded:", digest)
