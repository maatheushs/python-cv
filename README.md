# ATS-Friendly Resume Builder

Generate professional, ATS-optimized resumes tailored to specific job descriptions.

## Features

- **Interactive CLI** — Paste a job description and get a tailored resume
- **Keyword Analysis** — Automatically extract and match job keywords
- **Multiple Versions** — Define different resume versions per language (e.g. `default`, `backend_focused`, `full_stack`)
- **Bilingual** — English and Portuguese (PT-BR) support
- **DOCX & PDF Output** — ATS-friendly Word documents or PDF files
- **ATS Scoring** — Compatibility score with detailed feedback
- **JSON-based** — Easy to maintain and version-control your resume data

## Quick Start

### 1. Setup

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Your Data

Copy the example templates and fill in your information:

```bash
cp data/resume_en.example.json data/resume_en.json
cp data/resume_pt.example.json data/resume_pt.json
```

The JSON files support:
- Multiple **summary** versions (`default`, `backend_focused`, `full_stack`, etc.)
- Multiple **experience description** sets per job — tailor bullet points per version
- Categorized **skills**
- **Education** and **certifications**

See the existing example files for the full schema.

### 3. Run

```bash
python main.py
```

Follow the interactive prompts:
1. Choose language (English or PT-BR)
2. Choose output format (DOCX or PDF)
3. Paste a job description — or skip for a default resume
4. Review extracted keywords
5. Select a resume version (the tool recommends the best match)
6. Get your tailored resume with an ATS compatibility score

## Project Structure

```
python_cv/
├── main.py                          # Entry point
├── data/
│   ├── resume_en.json               # Resume data (English)
│   ├── resume_pt.json               # Resume data (Portuguese)
│   └── example_job_description.txt  # Sample job description for testing
├── application/
│   └── use_cases/                   # AnalyzeKeywords, GenerateResume, ScoreResume
├── domain/
│   ├── entities/                    # Resume, Experience, etc.
│   ├── services/                    # Domain services
│   └── value_objects/               # ATSScore, KeywordMatch
├── infrastructure/
│   ├── generators/                  # DocxResumeGenerator, PdfResumeGenerator
│   └── repositories/                # JsonResumeRepository
└── presentation/
    └── cli/                         # InteractiveCLI
```

## ATS Scoring

Your resume is scored on:

| Category           | Points |
|--------------------|--------|
| Contact Info       | 10     |
| Structure          | 20     |
| Keyword Match      | 30     |
| Experience Quality | 20     |
| Skills             | 10     |
| Achievements       | 10     |

**Target: 80+** for best ATS compatibility.

## Dependencies

- [`python-docx`](https://python-docx.readthedocs.io/) — DOCX generation
- [`reportlab`](https://www.reportlab.com/) — PDF generation
