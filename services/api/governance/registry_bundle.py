import json
import time
import hashlib
from services.api.governance.root_verifier import verify_root_signature
from services.api.governance.db import get_connection

def apply_registry_bundle(bundle: dict):

    message = json.dumps(bundle["registry"], sort_keys=True).encode()
    signature = bytes.fromhex(bundle["signature"])

    verify_root_signature(message, signature)

    conn = get_connection()
    cur = conn.cursor()

    for entry in bundle["registry"]:
        approver_id = entry["approver_id"]

        cur.execute("SELECT approver_id FROM approver_registry WHERE approver_id=?", (approver_id,))
        existing = cur.fetchone()

        if existing:
            cur.execute("""
                UPDATE approver_registry
                SET role=?, public_key=?, status=?, valid_from=?, valid_until=?, registry_signature=?
                WHERE approver_id=?
            """, (
                entry["role"],
                entry["public_key"],
                entry["status"],
                entry["valid_from"],
                entry["valid_until"],
                bundle["signature"],
                approver_id
            ))
        else:
            cur.execute("""
                INSERT INTO approver_registry
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                approver_id,
                entry["role"],
                entry["public_key"],
                entry["status"],
                entry["valid_from"],
                entry["valid_until"],
                bundle["signature"]
            ))

    conn.commit()
    conn.close()
