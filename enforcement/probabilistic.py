from monitoring.behavioral_monitor import BehavioralMonitor

monitor = BehavioralMonitor()

def enforce_probabilistic(action: dict):
    amount = float(action.get("amount", 0))
    score = monitor.anomaly_score(amount)

    if score > 0.7:
        return {
            "allowed": False,
            "reason": "Behavioral anomaly detected",
            "risk_score": score
        }

    monitor.record(amount)
    return {"allowed": True, "risk_score": score}
