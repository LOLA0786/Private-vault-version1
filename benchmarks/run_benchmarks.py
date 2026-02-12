from enforcement.engine import enforce
import time

cases = [
    {"amount": 500},
    {"amount": 2000},
    {"amount": 10000},
    {"amount": 75000},
]

start = time.time()
results = []

for case in cases:
    decision, replay_hash, ledger_valid = enforce(
        action={"tool": "transfer_funds", "amount": case["amount"]},
        principal={"trust_level": "high"},
    )
    results.append((case["amount"], decision["allowed"]))

end = time.time()

print("Results:", results)
print("Latency:", end - start)
