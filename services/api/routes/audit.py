from fastapi import APIRouter
from services.api.governance.store import audit_logs

router = APIRouter(prefix="/api/v1/audit", tags=["audit"])

@router.get("/")
async def list_audit():
    return audit_logs
