import statistics

class BehavioralMonitor:
    def __init__(self):
        self.history = []

    def record(self, amount: float):
        self.history.append(amount)

    def anomaly_score(self, amount: float) -> float:
        if len(self.history) < 5:
            return 0.0

        mean = statistics.mean(self.history)
        stdev = statistics.stdev(self.history) if len(self.history) > 1 else 0

        if stdev == 0:
            return 0.0

        z = abs((amount - mean) / stdev)
        return min(1.0, z / 5.0)
