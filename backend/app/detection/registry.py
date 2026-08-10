from app.detection.base import DetectionRule
from app.detection.rules import BruteForceRule


def get_detection_rules() -> list[DetectionRule]:
    return [
        BruteForceRule(),
    ]