from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    Flowable, HRFlowable, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle,
)

from application.interfaces.resume_generator import ResumeGenerator
from domain.entities.resume import Resume

_FONT_REGULAR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
_FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

pdfmetrics.registerFont(TTFont("DejaVu", _FONT_REGULAR))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", _FONT_BOLD))

DARK = colors.HexColor("#1a1a1a")
GRAY = colors.HexColor("#888888")
HR_DARK = colors.HexColor("#1a1a1a")
HR_LIGHT = colors.HexColor("#cccccc")

_PAGE_WIDTH, _PAGE_HEIGHT = A4
_MARGIN = 48  # pt

_S = {
    "name": ParagraphStyle(
        "name", fontName="Times-Bold", fontSize=28,
        textColor=DARK, alignment=TA_LEFT, spaceAfter=4, leading=32,
    ),
    "role": ParagraphStyle(
        "role", fontName="DejaVu", fontSize=9,
        textColor=GRAY, alignment=TA_LEFT, spaceAfter=3, leading=11, charSpace=1.5,
    ),
    "contact": ParagraphStyle(
        "contact", fontName="DejaVu", fontSize=9,
        textColor=GRAY, alignment=TA_LEFT, spaceAfter=0, leading=11,
    ),
    "job_title": ParagraphStyle(
        "job_title", fontName="DejaVu-Bold", fontSize=11,
        textColor=DARK, alignment=TA_LEFT, spaceAfter=2, leading=14,
    ),
    "job_date": ParagraphStyle(
        "job_date", fontName="DejaVu", fontSize=9,
        textColor=GRAY, alignment=TA_RIGHT, spaceAfter=2, leading=14,
    ),
    "company": ParagraphStyle(
        "company", fontName="DejaVu", fontSize=9,
        textColor=GRAY, alignment=TA_LEFT, spaceAfter=4, leading=11,
    ),
    "bullet": ParagraphStyle(
        "bullet", fontName="DejaVu", fontSize=10,
        textColor=GRAY, spaceAfter=0, leading=16.5, leftIndent=12,
    ),
    "body": ParagraphStyle(
        "body", fontName="DejaVu", fontSize=9.5,
        textColor=GRAY, spaceAfter=4, leading=15,
    ),
    "skill_label": ParagraphStyle(
        "skill_label", fontName="DejaVu-Bold", fontSize=9,
        textColor=GRAY, alignment=TA_LEFT, leading=13,
    ),
    "skill_tags": ParagraphStyle(
        "skill_tags", fontName="DejaVu", fontSize=9,
        textColor=GRAY, alignment=TA_LEFT, leading=13,
    ),
}

_HEADERS = {
    "en": {
        "summary": "Summary",
        "experience": "Experience",
        "skills": "Skills",
        "education": "Education",
        "certifications": "Certifications",
    },
    "pt": {
        "summary": "Resumo",
        "experience": "Experiência",
        "skills": "Habilidades",
        "education": "Formação",
        "certifications": "Certificações",
    },
}


class _SectionHeader(Flowable):
    """Section label left + hairline rule extending to right margin."""

    _FONT = "DejaVu"
    _SIZE = 8
    _CHAR_SPACE = 1.5
    _HEIGHT = 22

    def __init__(self, title: str, space_before: float = 20):
        super().__init__()
        self.title = title.upper()
        self.spaceBefore = space_before

    def wrap(self, avail_width, avail_height):
        self._avail_width = avail_width
        return avail_width, self._HEIGHT

    def draw(self):
        c = self.canv
        c.setFont(self._FONT, self._SIZE)
        c.setFillColor(GRAY)

        x, baseline = 0.0, 6.0
        for ch in self.title:
            c.drawString(x, baseline, ch)
            x += c.stringWidth(ch, self._FONT, self._SIZE) + self._CHAR_SPACE

        mid_y = baseline + self._SIZE / 2
        c.setStrokeColor(HR_LIGHT)
        c.setLineWidth(0.5)
        c.line(x + 8, mid_y, self._avail_width, mid_y)


def _two_col_table(left, right, avail_width, left_ratio=0.72):
    t = Table(
        [[left, right]],
        colWidths=[avail_width * left_ratio, avail_width * (1 - left_ratio)],
    )
    t.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, 0), "RIGHT"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return t


class PdfResumeGenerator(ResumeGenerator):
    def __init__(self):
        self._text_parts: list[str] = []

    def generate(self, resume: Resume, output_path: str) -> None:
        h = _HEADERS.get(resume.locale, _HEADERS["en"])
        p = resume.personal
        self._text_parts = []
        story = []

        avail_width = _PAGE_WIDTH - 2 * _MARGIN

        doc = SimpleDocTemplate(
            output_path, pagesize=A4,
            leftMargin=_MARGIN, rightMargin=_MARGIN,
            topMargin=_MARGIN, bottomMargin=_MARGIN,
        )

        # ── Header ──────────────────────────────────────────────────────────
        story.append(Paragraph(p.name, _S["name"]))
        story.append(Paragraph(p.title.upper(), _S["role"]))
        contact = f"{p.email}  ·  {p.phone}  ·  {p.location}  ·  {p.linkedin}"
        story.append(Paragraph(contact, _S["contact"]))
        story.append(Spacer(1, 10))
        story.append(HRFlowable(width="100%", thickness=2, color=HR_DARK, spaceAfter=0))
        self._text_parts += [p.name, p.title, p.phone, p.location, p.email, p.linkedin]

        # ── Summary ─────────────────────────────────────────────────────────
        story.append(_SectionHeader(h["summary"], space_before=16))
        story.append(Spacer(1, 4))
        story.append(Paragraph(resume.summary, _S["body"]))
        self._text_parts.append(resume.summary)

        # ── Experience ──────────────────────────────────────────────────────
        story.append(_SectionHeader(h["experience"]))
        for exp in resume.experience:
            story.append(Spacer(1, 10))
            story.append(_two_col_table(
                Paragraph(exp.position, _S["job_title"]),
                Paragraph(f"{exp.start_date} – {exp.end_date}", _S["job_date"]),
                avail_width,
            ))
            story.append(Paragraph(exp.company.upper(), _S["company"]))
            for item in exp.description:
                story.append(Paragraph(f"• {item}", _S["bullet"]))
                self._text_parts.append(item)

        # ── Skills ──────────────────────────────────────────────────────────
        story.append(_SectionHeader(h["skills"]))
        story.append(Spacer(1, 6))
        for category, skill_list in resume.skills.items():
            if not skill_list:
                continue
            label = category.replace("_", " ").title()
            tags = " · ".join(skill_list) if isinstance(skill_list, list) else skill_list
            row = _two_col_table(
                Paragraph(label, _S["skill_label"]),
                Paragraph(tags, _S["skill_tags"]),
                avail_width, left_ratio=0.26,
            )
            story.append(row)
            story.append(Spacer(1, 3))
            self._text_parts.append(tags)

        # ── Education ───────────────────────────────────────────────────────
        story.append(_SectionHeader(h["education"]))
        for edu in resume.education:
            story.append(Spacer(1, 10))
            story.append(_two_col_table(
                Paragraph(edu.institution, _S["job_title"]),
                Paragraph(f"{edu.start_date} – {edu.end_date}", _S["job_date"]),
                avail_width,
            ))
            story.append(Paragraph(edu.degree, _S["body"]))
            self._text_parts.append(edu.degree)

        # ── Certifications ──────────────────────────────────────────────────
        if resume.certifications:
            story.append(_SectionHeader(h["certifications"]))
            story.append(Spacer(1, 6))
            for cert in resume.certifications:
                story.append(Paragraph(
                    f"<b>{cert['name']}</b>  ·  {cert['issuer']}", _S["body"]
                ))

        doc.build(story)

    def get_text_content(self) -> str:
        return "\n".join(self._text_parts)
