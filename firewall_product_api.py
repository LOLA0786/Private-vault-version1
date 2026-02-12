from fastapi import FastAPI
from pydantic import BaseModel
import os

from firewall_core_logic import enforce_logic
from decision_ledger import DecisionLedger
from grok_gateway import call_grok_and_enforce

# ==========================================
# App Init
# ==========================================

app = FastAPI(title="PrivateVault AI Execution Firewall")

ledger = DecisionLedger()

# ==========================================
# Models
# ==========================================

class EnforceRequest(BaseModel):
    action: dict
    principal: dict
    context: dict | None = None


class GrokRequest(BaseModel):
    prompt: str
    principal: dict


class ModeRequest(BaseModel):
    mode: str


# ==========================================
# Enforcement Endpoint
# ==========================================

@app.post("/enforce")
def enforce(req: EnforceRequest):
    return enforce_logic(
        action=req.action,
        principal=req.principal,
        context=req.context or {}
    )


# ==========================================
# Grok Endpoint (Mandatory Firewall Gate)
# ==========================================

@app.post("/grok")
def grok(req: GrokRequest):
    return call_grok_and_enforce(
        prompt=req.prompt,
        principal=req.principal
    )


# ==========================================
# Runtime Mode Switch
# ==========================================

@app.post("/mode")
def set_mode(req: ModeRequest):
    os.environ["FIREWALL_MODE"] = req.mode.lower()
    return {"mode": os.environ["FIREWALL_MODE"]}


# ==========================================
# Audit Endpoints
# ==========================================

@app.get("/audit/merkle-root")
def get_merkle_root():
    return {
        "merkle_root": ledger.get_merkle_root()
    }


@app.get("/audit/verify")
def verify_ledger():
    try:
        ledger.verify_chain_integrity()
        return {"valid": True}
    except Exception as e:
        return {"valid": False, "error": str(e)}


@app.get("/audit/export")
def export_ledger():
    return {
        "events": ledger.events,
        "merkle_root": ledger.get_merkle_root()
    }

