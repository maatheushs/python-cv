from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ATSScore:
    score: float
    grade: str
    points: str
    feedback: List[str]

    def __str__(self) -> str:
        return f"{self.score}/100 ({self.grade})"
