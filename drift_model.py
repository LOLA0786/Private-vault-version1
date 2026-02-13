import numpy as np
from collections import deque

OUTPUT_HISTORY = deque(maxlen=200)

def detect_model_drift(output: str):

    length = len(output)

    if len(OUTPUT_HISTORY) < 10:
        OUTPUT_HISTORY.append(length)
        return {"drift_score": 0.0}

    mean = np.mean(OUTPUT_HISTORY)
    std = np.std(OUTPUT_HISTORY) or 1

    z_score = abs(length - mean) / std

    drift_score = min(z_score / 5, 1.0)

    OUTPUT_HISTORY.append(length)

    return {
        "drift_score": drift_score,
        "z_score": float(z_score),
        "mean_length": float(mean)
    }
