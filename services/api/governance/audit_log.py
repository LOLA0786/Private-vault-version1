from services.api.governance.store import audit_logs
from services.api.models.audit_model import AuditRecord
from datetime import datetime
import uuid

def log_event(actor: str, action: str, tenant_id: str, metadata: dict):
    record = AuditRecord(
        id=str(uuid.uuid4()),
        actor=actor,
        action=action,
        tenant_id=tenant_id,
        timestamp=datetime.utcnow(),
        metadata=metadata
    )
    audit_logs.append(record)
    return record
