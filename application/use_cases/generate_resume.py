from application.interfaces.resume_generator import ResumeGenerator
from domain.entities.resume import Resume


class GenerateResumeUseCase:
    def __init__(self, generators: dict):
        # dict: {"docx": DocxResumeGenerator, "pdf": PdfResumeGenerator}
        self._generators = generators

    def execute(self, resume: Resume, output_path: str, fmt: str = "docx") -> str:
        generator = self._generators.get(fmt, self._generators["docx"])
        generator.generate(resume, output_path)
        return generator.get_text_content()
