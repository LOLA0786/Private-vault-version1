from fastapi.testclient import TestClient
from firewall_product_api import app  # adjust to real file

client = TestClient(app)

def test_create_quorum():
    response = client.post(
        "/api/v1/quorum/",
        json={
            "id": "policy_update",
            "required_approvals": 2,
            "allowed_roles": ["admin"]
        },
        headers={"X-Role": "admin"}
    )

    assert response.status_code == 200
