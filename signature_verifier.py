import json
import nacl.signing
import nacl.exceptions
from typing import Dict


def canonical_json(data: Dict) -> bytes:
    """
    Deterministic JSON serialization for signing.
    """
    return json.dumps(
        data,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")


def verify_signature(public_key_hex: str, payload: Dict, signature_hex: str) -> bool:
    """
    Verify Ed25519 signature over canonical JSON payload.
    """
    try:
        verify_key = nacl.signing.VerifyKey(bytes.fromhex(public_key_hex))
        message = canonical_json(payload)
        verify_key.verify(message, bytes.fromhex(signature_hex))
        return True
    except (nacl.exceptions.BadSignatureError, Exception):
        return False
