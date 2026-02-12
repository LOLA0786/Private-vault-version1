from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class QuorumRule(BaseModel):
    id: str
    required_approvals: int
    allowed_roles: List[str]
    region: Optional[str] = None
    expiry: Optional[datetime] = None
