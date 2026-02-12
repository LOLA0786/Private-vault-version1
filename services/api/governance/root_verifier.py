from nacl.signing import VerifyKey
import os

def load_root_public_key():
    # High-security environment: HSM / mounted secure file
    path = os.getenv("ROOT_PUBLIC_KEY_PATH", "root_pub.key")
    with open(path, "rb") as f:
        return VerifyKey(f.read())

def verify_root_signature(message: bytes, signature: bytes):
    verify_key = load_root_public_key()
    verify_key.verify(message, signature)
