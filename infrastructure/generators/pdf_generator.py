from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import HRFlowable, Paragraph, SimpleDocTemplate, Spacer

from application.interfaces.resume_generator import ResumeGenerator
from domain.entities.resume import Resume

_FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
_FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

pdfmetrics.registerFont(TTFont("DejaVu", _FONT_REGULAR))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", _FONT_BOLD))

BLUE = colors.HexColor("#323296")
DARK = colors.HexColor("#1a1a1a")
GRAY = colors.HexColor("#555555")
HR_COLOR = colors.HexColor("#cccccc")

_STYLES = {
    "name": ParagraphStyle("name", fontName="DejaVu-Bold", fontSize=18, textColor=DARK,
                           alignment=TA_CENTER, spaceAfter=2),
    "subtitle": ParagraphStyle("subtitle", fontName="DejaVu", fontSize=12, textColor=GRAY,
                               alignment=TA_CENTER, spaceAfter=2),
    "contact": ParagraphStyle("contact", fontName="DejaVu", fontSize=10, textColor=GRAY,
                              alignment=TA_CENTER, spaceAfter=1),
    "section": ParagraphStyle("section", fontName="DejaVu-Bold", fontSize=12, textColor=BLUE,
                              spaceBefore=10, spaceAfter=2),
    "job_title": ParagraphStyle("job_title", fontName="DejaVu-Bold", fontSize=10, textColor=DARK,
                                spaceBefore=4, spaceAfter=2),
    "body": ParagraphStyle("body", fontName="DejaVu", fontSize=10, textColor=DARK,
                           spaceAfter=2, leading=14),
    "bullet": ParagraphStyle("bullet", fontName="DejaVu", fontSize=10, textColor=DARK,
                             spaceAfter=3, leading=14, leftIndent=12),
}

_HEADERS = {
    "en": {
        "summary": "Professional Summary",
        "experience": "Professional Experience",
        "skills": "Technical Skills",
        "education": "Education",
        "certifications": "Certifications",
    },
    "pt": {
        "summary": "Resumo Profissional",
        "experience": "Experiência Profissional",
        "skills": "Habilidades Técnicas",
        "education": "Formação Acadêmica",
        "certifications": "Certificações",
    },
}


def _hr():
    return HRFlowable(width="100%", thickness=0.5, color=HR_COLOR, spaceAfter=4)


class PdfResumeGenerator(ResumeGenerator):
    def __init__(self):
        self._text_parts: list[str] = []

    def generate(self, resume: Resume, output_path: str) -> None:
        h = _HEADERS.get(resume.locale, _HEADERS["en"])
        p = resume.personal
        story = []
        self._text_parts = []

        doc = SimpleDocTemplate(
            output_path, pagesize=A4,
            leftMargin=18 * mm, rightMargin=18 * mm,
            topMargin=16 * mm, bottomMargin=16 * mm,
        )

        # Header
        story.append(Paragraph(p.name, _STYLES["name"]))
        story.append(Paragraph(p.title, _STYLES["subtitle"]))
        story.append(Paragraph(f"{p.phone}  |  {p.location}", _STYLES["contact"]))
        story.append(Paragraph(f"{p.email}  |  {p.linkedin}", _STYLES["contact"]))
        story.append(Spacer(1, 4 * mm))
        self._text_parts += [p.name, p.title, p.phone, p.location, p.email, p.linkedin]

        # Summary
        story += [Paragraph(h["summary"].upper(), _STYLES["section"]), _hr()]
        story.append(Paragraph(resume.summary, _STYLES["body"]))
        self._text_parts.append(resume.summary)

        # Experience
        story += [Paragraph(h["experience"].upper(), _STYLES["section"]), _hr()]
        for exp in resume.experience:
            line = f"<b>{exp.position}</b>  –  {exp.company}  <font color='#777777'>({exp.start_date} – {exp.end_date})</font>"
            story.append(Paragraph(line, _STYLES["job_title"]))
            for item in exp.description:
                story.append(Paragraph(f"• {item}", _STYLES["bullet"]))
                self._text_parts.append(item)
            story.append(Spacer(1, 2 * mm))

        # Skills
        story += [Paragraph(h["skills"].upper(), _STYLES["section"]), _hr()]
        for category, skill_list in resume.skills.items():
            if not skill_list:
                continue
            label = category.replace("_", " ").title()
            skills_str = ", ".join(skill_list) if isinstance(skill_list, list) else skill_list
            story.append(Paragraph(f"<b>{label}:</b>  {skills_str}", _STYLES["body"]))
            self._text_parts.append(skills_str)

        # Education
        story += [Paragraph(h["education"].upper(), _STYLES["section"]), _hr()]
        for edu in resume.education:
            story.append(Paragraph(f"<b>{edu.institution}</b>", _STYLES["job_title"]))
            story.append(Paragraph(
                f"{edu.degree}  |  {edu.start_date} – {edu.end_date}", _STYLES["body"]
            ))
            self._text_parts.append(edu.degree)

        # Certifications
        if resume.certifications:
            story += [Paragraph(h["certifications"].upper(), _STYLES["section"]), _hr()]
            for cert in resume.certifications:
                story.append(Paragraph(f"<b>{cert['name']}</b> – {cert['issuer']}", _STYLES["body"]))

        doc.build(story)

    def get_text_content(self) -> str:
        return "\n".join(self._text_parts)
