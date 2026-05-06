from typing import List

from domain.services import keyword_analyzer
from domain.value_objects.keyword_match import KeywordMatch


class AnalyzeKeywordsUseCase:
    def extract(self, job_description: str, top_n: int = 30) -> List[str]:
        return keyword_analyzer.extract_keywords(job_description, top_n)

    def match(self, keywords: List[str], resume_text: str) -> KeywordMatch:
        return keyword_analyzer.match_keywords(keywords, resume_text)

    def suggest_version(self, keywords: List[str], available_versions: List[str]) -> str:
        return keyword_analyzer.suggest_version(keywords, available_versions)
