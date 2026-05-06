import json
from pathlib import Path
from typing import List

from application.interfaces.resume_repository import ResumeRepository
from domain.entities.resume import Education, Experience, PersonalInfo, Resume


class JsonResumeRepository(ResumeRepository):
    def __init__(self, data_path: str = "data/resume_data.json"):
        self._path = Path(data_path)
        self._raw = self._load_raw()

    def _load_raw(self) -> dict:
        with self._path.open(encoding="utf-8") as f:
            return json.load(f)

    def get_available_versions(self) -> List[str]:
        summary = self._raw.get("summary", {})
        if isinstance(summary, dict):
            return list(summary.keys())
        return ["default"]

    def load(self, version: str = "default") -> Resume:
        raw = self._raw

        personal = PersonalInfo(**raw["personal"])

        summary_raw = raw.get("summary", "")
        summary = (
            summary_raw.get(version, summary_raw.get("default", ""))
            if isinstance(summary_raw, dict)
            else summary_raw
        )

        experience = [
            Experience(
                company=exp["company"],
                position=exp["position"],
                location=exp["location"],
                start_date=exp["start_date"],
                end_date=exp["end_date"],
                description=self._pick_description(exp, version),
            )
            for exp in raw.get("experience", [])
        ]

        education = [
            Education(
                institution=edu["institution"],
                degree=edu["degree"],
                location=edu.get("location", ""),
                start_date=edu["start_date"],
                end_date=edu["end_date"],
            )
            for edu in raw.get("education", [])
        ]

        return Resume(
            personal=personal,
            summary=summary,
            experience=experience,
            skills=raw.get("skills", {}),
            education=education,
            certifications=raw.get("certifications", []),
            locale=raw.get("locale", "en"),
        )

    @staticmethod
    def _pick_description(exp: dict, version: str) -> List[str]:
        descriptions = exp.get("descriptions", {})
        if isinstance(descriptions, dict):
            return descriptions.get(version, descriptions.get("default", []))
        return exp.get("description", [])
