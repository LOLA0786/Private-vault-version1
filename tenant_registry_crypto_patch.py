from cryptography.fernet import Fernet
import os

_cipher = None

def get_cipher():
    global _cipher
    if _cipher is None:
        key = os.getenv("TENANT_MASTER_KEY")
        if not key:
            raise RuntimeError("TENANT_MASTER_KEY not set")
        _cipher = Fernet(key.strip().encode())
    return _cipher
