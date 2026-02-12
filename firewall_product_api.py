from enterprise_governance_v1.registry import load_registry_bundle
from enterprise_governance_v1.policy import load_policy_bundle

from tenant_registry import get_signing_key, get_provider_api_key
from signature_verifier import verify_signature, canonical_json
from replay_protection import check_replay
from fastapi import FastAPI, Request
from pydantic import BaseModel
import os

from firewall_core_logic import enforce_logic
from decision_ledger import DecisionLedger
from grok_gateway import call_grok_and_enforce

# ==========================================
# App Init
# ==========================================

app = FastAPI(title="PrivateVault AI Execution Firewall")

from config import get_settings

@app.on_event("startup")
async def validate_environment():
    settings = get_settings()
    from services.api.governance.db import init_db
    init_db()
    if not settings.tenant_master_key:
        raise RuntimeError("TENANT_MASTER_KEY not set")

# --- Governance Layer Injection ---
from services.api.routes import quorum, approvals, audit
from services.api.governance.middleware import RoleTenantMiddleware

app.add_middleware(RoleTenantMiddleware)
app.include_router(quorum.router)
app.include_router(approvals.router)
app.include_router(audit.router)
# --- End Governance Injection ---

ledger = DecisionLedger()

# ==========================================
# Models
# ==========================================

class EnforceRequest(BaseModel):
    action: dict
    principal: dict
    nonce: str
    timestamp: float
    signature: str
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
    # --- Signature Verification ---
    tenant_id = req.principal.get("tenant_id", "default")
    signing_key = get_signing_key(tenant_id)

    if not signing_key:
        return {"allowed": False, "layer": "auth", "reason": "Unregistered tenant"}

    signed_payload = {
        "action": req.action,
        "principal": req.principal,
        "nonce": req.nonce,
        "timestamp": req.timestamp,
        "context": req.context or {}
    }

    if not verify_signature(signing_key, signed_payload, req.signature):
        return {"allowed": False, "layer": "signature_verification", "reason": "Invalid signature"}


        return {"allowed": False, "layer": "signature_verification", "reason": "Invalid signature"}

    # --- Replay Protection ---
    tenant_id = req.principal.get("tenant_id", "default")
    if not check_replay(tenant_id, req.nonce, req.timestamp):
        return {"allowed": False, "layer": "replay_protection", "reason": "Replay or invalid timestamp"}

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
def set_mode(req: ModeRequest, request: Request):
    from services.api.governance.governance_guard import assert_action_approved
    assert_action_approved("mode_change", request)
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


@app.on_event("startup")
def governance_startup():
    load_registry_bundle("registry_bundle.json")
    load_policy_bundle("policy_bundle.json")

