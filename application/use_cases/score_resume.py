from typing import Optional

from domain.entities.resume import Resume
from domain.services import ats_scorer
from domain.value_objects.ats_score import ATSScore


class ScoreResumeUseCase:
    def execute(
        self,
        resume: Resume,
        resume_text: str,
        keyword_match_rate: Optional[float] = None,
    ) -> ATSScore:
        return ats_scorer.score_resume(resume, resume_text, keyword_match_rate)
