from fastapi import APIRouter, HTTPException
from services.api.governance.db import get_connection
from services.api.governance.quorum_engine import evaluate_action
import uuid
import time

router = APIRouter(prefix="/api/v1/approvals", tags=["approvals"])

@router.post("/{action_id}/approve")
async def approve(action_id: str, approver_id: str, role: str, signature: str):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM governance_action WHERE id=?", (action_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Action not found")

    approval_id = str(uuid.uuid4())
    ts = int(time.time())

    cur.execute("""
        INSERT INTO approval
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        approval_id,
        action_id,
        1,
        approver_id,
        role,
        signature,
        ts
    ))

    conn.commit()
    conn.close()

    evaluate_action(action_id)

    return {"status": "processed"}
