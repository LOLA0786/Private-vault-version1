from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class Approval(BaseModel):
    id: str
    action: str
    tenant_id: str
    requested_by: str
    approvals: List[str] = []
    created_at: datetime
    status: str = "pending"
