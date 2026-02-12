import hashlib
import json
import time
import uuid
from services.api.governance.db import get_connection

def append_audit(action_id, event_type, data):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT current_hash FROM governance_audit ORDER BY timestamp DESC LIMIT 1")
    prev = cur.fetchone()
    prev_hash = prev[0] if prev else ""

    payload = json.dumps(data, sort_keys=True)
    base = f"{action_id}{event_type}{payload}{prev_hash}{int(time.time())}"
    current_hash = hashlib.sha256(base.encode()).hexdigest()

    cur.execute("""
        INSERT INTO governance_audit
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        str(uuid.uuid4()),
        action_id,
        event_type,
        payload,
        prev_hash,
        current_hash,
        int(time.time())
    ))

    conn.commit()
    conn.close()
