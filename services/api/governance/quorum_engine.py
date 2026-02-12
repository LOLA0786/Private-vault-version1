import json
import time
from services.api.governance.db import get_connection
from services.api.governance.signature_verifier import verify_signature

def evaluate_action(action_id: str):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT action_type, payload_hash, current_layer FROM governance_action WHERE id=?", (action_id,))
    row = cur.fetchone()
    if not row:
        return False

    action_type, payload_hash, current_layer = row

    cur.execute("SELECT layers_json FROM governance_policy WHERE action_type=? AND tenant_id IS ??", (action_type,))
    policy = cur.fetchone()
    if not policy:
        return False

    layers = json.loads(policy[0])
    if current_layer > len(layers):
        return True

    layer = layers[current_layer - 1]
    threshold = layer["threshold"]
    allowed_roles = set(layer["roles"])

    cur.execute("SELECT approver_id, role, signature, timestamp FROM approval WHERE action_id=? AND layer_index=?", (action_id, current_layer))
    approvals = cur.fetchall()

    valid_count = 0
    used = set()

    for approver_id, role, signature, ts in approvals:
        if role not in allowed_roles:
            continue
        if approver_id in used:
            continue

        cur.execute("SELECT public_key, status FROM approver_registry WHERE approver_id=?", (approver_id,))
        reg = cur.fetchone()
        if not reg:
            continue

        public_key, status = reg
        if status != "active":
            continue

        message = f"{action_id}{payload_hash}{current_layer}{approver_id}{ts}".encode()

        if verify_signature(public_key, message, signature):
            valid_count += 1
            used.add(approver_id)

    if valid_count >= threshold:
        if current_layer == len(layers):
            cur.execute("UPDATE governance_action SET status='approved' WHERE id=?", (action_id,))
        else:
            cur.execute("UPDATE governance_action SET current_layer=? WHERE id=?", (current_layer + 1, action_id))
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False
