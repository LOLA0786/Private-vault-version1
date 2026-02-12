import json
import os
from typing import Optional, Dict
from cryptography.fernet import Fernet

REGISTRY_FILE = "tenant_registry.json"

MASTER_KEY = os.getenv("TENANT_MASTER_KEY")

if not MASTER_KEY:
    raise RuntimeError("TENANT_MASTER_KEY not set")

cipher = Fernet(MASTER_KEY.encode())


def _load_registry() -> Dict:
    if not os.path.exists(REGISTRY_FILE):
        return {}
    with open(REGISTRY_FILE, "r") as f:
        return json.load(f)


def _save_registry(registry: Dict):
    with open(REGISTRY_FILE, "w") as f:
        json.dump(registry, f, indent=2)


def register_tenant(
    tenant_id: str,
    signing_public_key: str,
    provider_api_key: str
):
    registry = _load_registry()

    encrypted_provider_key = cipher.encrypt(
        provider_api_key.encode()
    ).decode()

    registry[tenant_id] = {
        "signing_public_key": signing_public_key,
        "provider_api_key": encrypted_provider_key
    }

    _save_registry(registry)


def get_signing_key(tenant_id: str) -> Optional[str]:
    registry = _load_registry()
    tenant = registry.get(tenant_id)
    if not tenant:
        return None
    return tenant.get("signing_public_key")


def get_provider_api_key(tenant_id: str) -> Optional[str]:
    registry = _load_registry()
    tenant = registry.get(tenant_id)
    if not tenant:
        return None

    encrypted = tenant.get("provider_api_key")
    if not encrypted:
        return None

    return cipher.decrypt(encrypted.encode()).decode()
