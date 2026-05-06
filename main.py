#!/usr/bin/env python3
from application.use_cases.analyze_keywords import AnalyzeKeywordsUseCase
from application.use_cases.generate_resume import GenerateResumeUseCase
from application.use_cases.score_resume import ScoreResumeUseCase
from infrastructure.generators.docx_generator import DocxResumeGenerator
from infrastructure.generators.pdf_generator import PdfResumeGenerator
from infrastructure.repositories.json_resume_repository import JsonResumeRepository
from presentation.cli.interactive_cli import InteractiveCLI

_LANG_FILES = {
    "en": "data/resume_en.json",
    "pt": "data/resume_pt.json",
}


def repository_factory(lang: str) -> JsonResumeRepository:
    return JsonResumeRepository(_LANG_FILES.get(lang, _LANG_FILES["en"]))


def main():
    cli = InteractiveCLI(
        analyze_keywords=AnalyzeKeywordsUseCase(),
        generate_resume=GenerateResumeUseCase({
            "docx": DocxResumeGenerator(),
            "pdf": PdfResumeGenerator(),
        }),
        score_resume=ScoreResumeUseCase(),
    )

    cli.run(repository_factory)


if __name__ == "__main__":
    main()
