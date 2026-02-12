from typing import Dict, List
from services.api.models.quorum_model import QuorumRule
from services.api.models.approval_model import Approval
from services.api.models.audit_model import AuditRecord

quorum_rules: Dict[str, QuorumRule] = {}
approvals: Dict[str, Approval] = {}
audit_logs: List[AuditRecord] = []
