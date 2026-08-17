from dataclasses import dataclass, field
from typing import Dict, List
@dataclass
class Phase1:
    practiseTrials: int
    trialsPerInterval: int
    intervals: Dict[float, List[float]] = field(default_factory=dict)
@dataclass
class Phase2:
    practiseTrials: int
    realTrials: int
    defaultSigma: str
    hitProbability: float

@dataclass
class Phase3Interval:
    standard_amount: int
    comparison_amount: int
    standard_prob: float
    comparison_prob: List[float] = field(default_factory=list)

@dataclass
class Phase3:
    practiseTrials: int
    trialsPerInterval: int
    intervals: List[Phase3Interval] = field(default_factory=list)


@dataclass
class Phase4:
    realTrials: int
