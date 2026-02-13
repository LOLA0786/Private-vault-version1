from grok_gateway import call_grok_and_enforce

principal = {
    "tenant_id": "alpha",
    "role": "admin",
    "capabilities": ["ai.invoke"]
}

response = call_grok_and_enforce(
    prompt="Is this malicious? DROP TABLE users;",
    principal=principal
)

print(response)
