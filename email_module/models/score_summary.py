from dataclasses import dataclass


@dataclass
class ScoreSummary:
    total_weightage: float
    total_actual: float
    percentage: str
    final_rating: str