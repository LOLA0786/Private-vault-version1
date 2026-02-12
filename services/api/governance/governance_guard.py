from fastapi import HTTPException, Request
from services.api.governance.store import approvals
from services.api.governance.quorum_engine import evaluate_quorum
from services.api.governance.config import ENABLE_GOVERNANCE
from config import get_settings


def assert_action_approved(action: str, request: Request):

    settings = get_settings()

    # If governance disabled → allow
    if not settings.enable_governance:
        return

    # Dev environment bypass
    if settings.environment != "production":
        return

    # Look for approved action
    for approval in approvals.values():
        if approval.action == action and approval.status == "approved":
            return

    raise HTTPException(status_code=403, detail="Governance approval required")
