import hashlib
import json
import os
from datetime import datetime


class DecisionLedger:
    def __init__(self, filepath="ledger.json"):
        self.filepath = filepath
        self.chain = []

        if os.path.exists(self.filepath):
            with open(self.filepath, "r") as f:
                try:
                    self.chain = json.load(f)
                except:
                    self.chain = []

    def _hash(self, block):
        return hashlib.sha256(
            json.dumps(block, sort_keys=True).encode()
        ).hexdigest()

    def log(self, event: dict):
        previous_hash = self.chain[-1]["hash"] if self.chain else "GENESIS"

        block = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "previous_hash": previous_hash,
        }

        block["hash"] = self._hash(block)

        self.chain.append(block)

        with open(self.filepath, "w") as f:
            json.dump(self.chain, f, indent=2)

        return block["hash"]

    def verify(self):
        prev = "GENESIS"

        for block in self.chain:
            recalculated = self._hash({
                "timestamp": block["timestamp"],
                "event": block["event"],
                "previous_hash": block["previous_hash"],
            })

            if recalculated != block["hash"]:
                return False

            if block["previous_hash"] != prev:
                return False

            prev = block["hash"]

        return True
