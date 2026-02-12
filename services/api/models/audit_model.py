from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AuditRecord(BaseModel):
    id: str
    actor: str
    action: str
    tenant_id: Optional[str]
    timestamp: datetime
    metadata: dict
