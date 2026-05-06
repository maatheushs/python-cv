from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class KeywordMatch:
    matched: List[str]
    missing: List[str]
    match_rate: float
    total_keywords: int

    def __str__(self) -> str:
        return f"{len(self.matched)}/{self.total_keywords} ({self.match_rate}%)"
