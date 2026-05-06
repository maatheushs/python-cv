import re
from typing import Dict, List, Optional

from domain.entities.resume import Resume
from domain.value_objects.ats_score import ATSScore


def score_resume(resume: Resume, resume_text: str, keyword_match_rate: Optional[float] = None) -> ATSScore:
    points = 0
    feedback: List[str] = []

    points += _score_contact(resume.personal.__dict__, feedback)
    points += _score_structure(resume, feedback)
    if keyword_match_rate is not None:
        points += _score_keywords(keyword_match_rate, feedback)
    points += _score_experience(resume.experience, feedback)
    points += _score_skills(resume.skills, feedback)
    points += _score_achievements(resume.experience, feedback)

    max_points = 100 if keyword_match_rate is not None else 70
    final = round((points / max_points) * 100, 1)

    return ATSScore(
        score=final,
        grade=_grade(final),
        points=f"{points}/{max_points}",
        feedback=feedback,
    )


def _score_contact(personal: Dict, feedback: List[str]) -> int:
    required = ['name', 'email', 'phone', 'location']
    optional = ['linkedin', 'github']
    pts = (sum(1 for f in required if personal.get(f)) / len(required)) * 7
    pts += min(3, sum(1 for f in optional if personal.get(f)) * 1.5)
    feedback.append("✓ Contact information is complete" if pts >= 8 else "⚠ Missing some contact information")
    return round(pts)


def _score_structure(resume: Resume, feedback: List[str]) -> int:
    sections = [resume.personal, resume.summary, resume.experience, resume.skills, resume.education]
    present = sum(1 for s in sections if s)
    pts = (present / len(sections)) * 20
    feedback.append("✓ Resume has all essential sections" if present >= 4 else "⚠ Resume is missing some sections")
    return round(pts)


def _score_keywords(match_rate: float, feedback: List[str]) -> int:
    pts = (match_rate / 100) * 30
    if match_rate >= 70:
        feedback.append(f"✓ Excellent keyword match: {match_rate}%")
    elif match_rate >= 50:
        feedback.append(f"⚠ Good keyword match: {match_rate}% (aim for 70%+)")
    else:
        feedback.append(f"✗ Low keyword match: {match_rate}% (needs improvement)")
    return round(pts)


def _score_experience(experiences: list, feedback: List[str]) -> int:
    if not experiences:
        feedback.append("✗ No work experience listed")
        return 0
    n = len(experiences)
    pts = (sum(1 for e in experiences if e.start_date and e.end_date) / n) * 5
    pts += (sum(1 for e in experiences if e.location) / n) * 5
    pts += (sum(1 for e in experiences if e.description) / n) * 10
    feedback.append("✓ Work experience is well-documented" if pts >= 16 else "⚠ Work experience could be more detailed")
    return round(pts)


def _score_skills(skills: Dict, feedback: List[str]) -> int:
    total = sum(len(v) for v in skills.values() if isinstance(v, list))
    if total >= 15:
        feedback.append(f"✓ Strong skills section ({total} skills listed)")
        return 10
    elif total >= 10:
        feedback.append(f"⚠ Good skills section ({total} skills, aim for 15+)")
        return 7
    feedback.append(f"⚠ Add more skills ({total} listed, aim for 15+)")
    return 4


def _score_achievements(experiences: list, feedback: List[str]) -> int:
    patterns = [r'\d+%', r'\d+x', r'\$[\d,]+', r'\d+\s*(hours|days|weeks|months)',
                r'(increased|decreased|reduced|improved|grew)\s+by\s+\d+']
    count = sum(
        1 for exp in experiences
        for desc in exp.description
        if any(re.search(p, desc, re.IGNORECASE) for p in patterns)
    )
    if count >= 3:
        feedback.append(f"✓ Great use of quantifiable achievements ({count} found)")
        return 10
    elif count >= 1:
        feedback.append(f"⚠ Some quantifiable achievements ({count} found, aim for 3+)")
        return 6
    feedback.append("✗ Add quantifiable achievements (percentages, numbers, metrics)")
    return 0


def _grade(score: float) -> str:
    if score >= 90:
        return "A (Excellent)"
    if score >= 80:
        return "B (Good)"
    if score >= 70:
        return "C (Fair)"
    if score >= 60:
        return "D (Needs Improvement)"
    return "F (Poor)"
