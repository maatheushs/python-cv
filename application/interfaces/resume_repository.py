from abc import ABC, abstractmethod
from typing import List

from domain.entities.resume import Resume


class ResumeRepository(ABC):
    @abstractmethod
    def load(self, version: str = "default") -> Resume:
        ...

    @abstractmethod
    def get_available_versions(self) -> List[str]:
        ...
