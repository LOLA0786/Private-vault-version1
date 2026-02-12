from nacl.signing import VerifyKey
from nacl.exceptions import BadSignatureError
import base64

def verify_signature(public_key_hex: str, message: bytes, signature_hex: str):
    try:
        verify_key = VerifyKey(bytes.fromhex(public_key_hex))
        verify_key.verify(message, bytes.fromhex(signature_hex))
        return True
    except BadSignatureError:
        return False
