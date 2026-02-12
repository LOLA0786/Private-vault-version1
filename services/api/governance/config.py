import os

ENABLE_GOVERNANCE = os.getenv("ENABLE_GOVERNANCE", "true").lower() == "true"
MIN_APPROVALS = int(os.getenv("MIN_APPROVALS", "2"))
