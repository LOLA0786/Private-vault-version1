import hashlib
import json
import time
from fastapi import HTTPException
from services.api.governance.db import get_connection

def assert_action_allowed(action_type: str, tenant_id: str, payload: dict):

    payload_hash = hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode()
    ).hexdigest()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT id, cooldown_until, consumed, expires_at
        FROM governance_action
        WHERE action_type=? AND tenant_id IS ?
        AND payload_hash=? AND status='approved'
    """, (action_type, tenant_id, payload_hash))

    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=403, detail="Governance approval required")

    action_id, cooldown_until, consumed, expires_at = row

    now = int(time.time())

    if expires_at and expires_at < now:
        conn.close()
        raise HTTPException(status_code=403, detail="Approval expired")

    if consumed:
        conn.close()
        raise HTTPException(status_code=403, detail="Action already consumed")

    if cooldown_until and cooldown_until > now:
        conn.close()
        raise HTTPException(status_code=403, detail="Cooldown active")

    cur.execute("UPDATE governance_action SET consumed=1 WHERE id=?", (action_id,))
    conn.commit()
    conn.close()
