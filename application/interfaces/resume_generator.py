from abc import ABC, abstractmethod

from domain.entities.resume import Resume


class ResumeGenerator(ABC):
    @abstractmethod
    def generate(self, resume: Resume, output_path: str) -> None:
        ...

    @abstractmethod
    def get_text_content(self) -> str:
        ...
