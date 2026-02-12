from fastapi import FastAPI
from firewall import enforce

app = FastAPI(title="PrivateVault Execution Firewall")

@app.post("/enforce")
def enforce_action(payload: dict):

    action = payload.get("action")
    principal = payload.get("principal", {})
    context = payload.get("context", {})

    result = enforce(action, principal, context)

    return result
