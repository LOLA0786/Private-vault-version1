from firewall import enforce

request = {
    "tenant_id": "alpha",
    "content": "DROP TABLE users;"
}

result = enforce(request)
print(result)
