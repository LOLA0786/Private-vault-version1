from policy_engine import evaluate_policy

request = {
    "tenant_id": "alpha",
    "content": "DROP TABLE users;"
}

decision = evaluate_policy(request)
print(decision)
