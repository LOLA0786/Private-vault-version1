import json
import time
import hashlib
from services.api.governance.root_verifier import verify_root_signature
from services.api.governance.db import get_connection

def apply_policy_bundle(bundle: dict):

    message = json.dumps(bundle["policy"], sort_keys=True).encode()
    signature = bytes.fromhex(bundle["signature"])

    verify_root_signature(message, signature)

    conn = get_connection()
    cur = conn.cursor()

    policy = bundle["policy"]

    cur.execute("""
        SELECT version FROM governance_policy
        WHERE action_type=? AND tenant_id IS ?
    """, (policy["action_type"], policy["tenant_id"]))

    existing = cur.fetchone()

    if existing:
        if policy["version"] <= existing[0]:
            conn.close()
            raise Exception("Policy rollback or stale version detected")

        cur.execute("""
            UPDATE governance_policy
            SET layers_json=?, expires_in_seconds=?, cooldown_seconds=?, version=?, policy_hash=?, signature=?, created_at=?
            WHERE action_type=? AND tenant_id IS ?
        """, (
            json.dumps(policy["layers"]),
            policy["expires_in_seconds"],
            policy["cooldown_seconds"],
            policy["version"],
            policy["policy_hash"],
            bundle["signature"],
            int(time.time()),
            policy["action_type"],
            policy["tenant_id"]
        ))
    else:
        cur.execute("""
            INSERT INTO governance_policy
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            policy["id"],
            policy["action_type"],
            policy["tenant_id"],
            json.dumps(policy["layers"]),
            policy["expires_in_seconds"],
            policy["cooldown_seconds"],
            policy["version"],
            policy["policy_hash"],
            bundle["signature"],
            int(time.time())
        ))

    conn.commit()
    conn.close()
