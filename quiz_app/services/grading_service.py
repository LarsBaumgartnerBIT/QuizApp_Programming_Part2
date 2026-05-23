from __future__ import annotations
from typing import Iterable, Tuple

class GradingService:
    def __init__(
        self,
        min_grade: float = 1.0,
        max_grade: float = 6.0,
        pass_grade: float = 4.0,
    ) -> None:
        self.min_grade = min_grade
        self.max_grade = max_grade
        self.pass_grade = pass_grade

    def evaluate(self, correct_flags: Iterable[bool]) -> Tuple[int, float, float]:
        flags = list(correct_flags)
        num_total = len(flags)
        num_correct = sum(1 for flag in flags if flag)
        if num_total == 0:
            return 0, 0.0, self.min_grade
        fraction = num_correct / num_total
        score_percent = round(100.0 * fraction, 1)
        grade = round(self.min_grade + fraction * (self.max_grade - self.min_grade), 1)
        return num_correct, score_percent, grade
    def is_passing(self, grade: float) -> bool:
        return grade >= self.pass_grade
