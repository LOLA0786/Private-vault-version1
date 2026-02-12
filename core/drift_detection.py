"""
Behavioral Drift Detection Engine
Semantic alignment threshold-based blocking.
"""

DRIFT_VERSION = "v2_threshold"

DEFAULT_THRESHOLD = 0.7


class DriftDetector:

    def __init__(self, threshold=DEFAULT_THRESHOLD):
        self.threshold = threshold

    def calculate_alignment(self, prompt: str, actions: list):
        prompt_tokens = set(prompt.lower().split())
        action_tokens = set(str(actions).lower().split())

        if not action_tokens:
            return 0.0

        intersection = prompt_tokens.intersection(action_tokens)
        score = len(intersection) / max(len(prompt_tokens), 1)
        return score

    def detect(self, prompt: str, actions: list):
        score = self.calculate_alignment(prompt, actions)

        should_block = score < self.threshold

        return {
            "drift_version": DRIFT_VERSION,
            "alignment_score": score,
            "threshold": self.threshold,
            "should_block": should_block
        }
