from fastapi import APIRouter, Depends, HTTPException
from services.api.models.quorum_model import QuorumRule
from services.api.governance.store import quorum_rules
from services.api.governance.config import ENABLE_GOVERNANCE

router = APIRouter(prefix="/api/v1/quorum", tags=["quorum"])

@router.post("/")
async def create_quorum(rule: QuorumRule):
    if not ENABLE_GOVERNANCE:
        raise HTTPException(status_code=403, detail="Governance disabled")

    quorum_rules[rule.id] = rule
    return rule

@router.get("/")
async def list_quorums():
    return list(quorum_rules.values())
