from fastapi import FastAPI
from pydantic import BaseModel
from core.policy_engine import authorize_intent
from core.drift_detection import DriftDetector
from core.decision_ledger import DecisionLedger

app = FastAPI(title="PrivateVault AI Execution Firewall")

drift = DriftDetector(threshold=0.7)
ledger = DecisionLedger()

class EnforceRequest(BaseModel):
    action: dict
    principal: dict
    context: dict | None = None

@app.post("/enforce")
def enforce(req: EnforceRequest):

    context = req.context or {}

    # 1️⃣ Deterministic
    policy = authorize_intent(
        req.action,
        principal=req.principal,
        context=context
    )

    if not policy["allowed"]:
        ledger.log_event("deterministic_block", policy)
        return {
            "allowed": False,
            "layer": "deterministic",
            "reason": policy["reason"]
        }

    # 2️⃣ Drift
    drift_result = drift.detect(
        prompt=str(req.action),
        actions=[req.action]
    )

    if drift_result.get("should_block"):
        ledger.log_event("drift_block", drift_result)
        return {
            "allowed": False,
            "layer": "behavioral",
            "reason": drift_result.get("reason")
        }

    # 3️⃣ Approved
    ledger.log_event("approved", req.action)

    return {
        "allowed": True,
        "layer": "approved"
    }

