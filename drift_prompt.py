import re
import hashlib
import time
from collections import deque

# Simple rolling history
PROMPT_HISTORY = deque(maxlen=100)

SUSPICIOUS_PATTERNS = [
    r"ignore .* instructions",
    r"override .* policy",
    r"reveal .* credentials",
    r"bypass .* security",
    r"send .* secrets",
    r"internal .* key",
]

def _hash_prompt(prompt: str) -> str:
    return hashlib.sha256(prompt.encode()).hexdigest()

def _pattern_score(prompt: str) -> float:
    score = 0
    for pattern in SUSPICIOUS_PATTERNS:
        if re.search(pattern, prompt.lower()):
            score += 0.3
    return min(score, 1.0)

def detect_prompt_drift(prompt: str):
    prompt_hash = _hash_prompt(prompt)
    pattern_risk = _pattern_score(prompt)

    historical_match = sum(
        1 for p in PROMPT_HISTORY if p["hash"] == prompt_hash
    )

    novelty_score = 1.0 if historical_match == 0 else 0.1

    drift_score = min(pattern_risk + novelty_score * 0.5, 1.0)

    PROMPT_HISTORY.append({
        "hash": prompt_hash,
        "timestamp": time.time()
    })

    return {
        "drift_score": drift_score,
        "pattern_risk": pattern_risk,
        "novelty_score": novelty_score
    }
