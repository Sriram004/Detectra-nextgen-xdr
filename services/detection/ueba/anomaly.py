from dataclasses import dataclass


@dataclass
class Baseline:
    mean: float
    stddev: float


def zscore(value: float, baseline: Baseline) -> float:
    if baseline.stddev == 0:
        return 0.0
    return (value - baseline.mean) / baseline.stddev


def is_anomalous(value: float, baseline: Baseline, threshold: float = 3.0) -> bool:
    return abs(zscore(value, baseline)) >= threshold
