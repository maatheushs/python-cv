# Resume Builder

A command-line tool that generates tailored, ATS-friendly resumes in PDF or DOCX — with keyword matching against a job description.

---

## What this does

1. You paste a job description
2. It extracts the relevant keywords
3. It picks the best resume version for that job
4. It generates a ready-to-send PDF or Word file

---

## Setup (first time only)

**Requirements:** Python 3.10+

```bash
# 1. Clone the repo
git clone <repo-url>
cd python_cv

# 2. Create a virtual environment
python3 -m venv venv

# 3. Activate it
source venv/bin/activate        # macOS / Linux / WSL
# venv\Scripts\activate         # Windows CMD

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create your resume data files from the templates
cp data/resume_en.example.json data/resume_en.json
cp data/resume_pt.example.json data/resume_pt.json
```

Now open `data/resume_en.json` and `data/resume_pt.json` and replace the placeholder values with your real information.

> Your personal data files are listed in `.gitignore` and will never be committed to git.

---

## Running

```bash
source venv/bin/activate   # skip if already active
python main.py
```

The tool will ask:

1. **Language** — English or Portuguese
2. **Format** — PDF or DOCX
3. **Job description** — paste it and press Enter twice, or skip for a default resume
4. **Resume version** — the tool recommends the best match; you can pick another

The generated file is saved to your Documents folder automatically.

---

## Customizing your resume

Your JSON files support multiple **versions** of each section. This lets you have different bullet points and summaries depending on the type of role you're applying for — without maintaining separate files.

```json
{
  "personal": {
    "name": "Your Name",
    "title": "Software Engineer",
    "phone": "+1 555 000 1234",
    "email": "you@example.com",
    "location": "City, Country",
    "linkedin": "linkedin.com/in/yourhandle",
    "github": "github.com/yourhandle"
  },

  "summary": {
    "default":          "A general summary that works for most roles.",
    "backend_focused":  "A summary emphasizing backend and systems work.",
    "full_stack":       "A summary emphasizing end-to-end delivery."
  },

  "experience": [
    {
      "company": "Acme Corp",
      "position": "Software Engineer",
      "start_date": "2021",
      "end_date": "2024",
      "descriptions": {
        "default":         ["Bullet 1", "Bullet 2"],
        "backend_focused": ["Different bullet 1", "Different bullet 2"]
      }
    }
  ],

  "skills": {
    "backend":   ["Node.js", "NestJS"],
    "databases": ["PostgreSQL", "Redis"]
  },

  "education": [
    {
      "institution": "University Name",
      "degree": "Degree Name",
      "start_date": "2016",
      "end_date": "2020"
    }
  ],

  "certifications": []
}
```

When you paste a job description, the tool scores each version against it and picks the one with the highest keyword match. You can always override and pick manually.

---

## Project structure

```
python_cv/
├── main.py                            # Entry point — run this
├── data/
│   ├── resume_en.json                 # Your resume in English       (git-ignored)
│   ├── resume_pt.json                 # Your resume in Portuguese    (git-ignored)
│   ├── resume_en.example.json         # Template — copy and fill in
│   ├── resume_pt.example.json         # Template — copy and fill in
│   └── example_job_description.txt    # Sample job description for testing
├── application/use_cases/             # Keyword analysis, resume generation, ATS scoring
├── domain/                            # Entities and business rules
├── infrastructure/generators/         # PDF and DOCX output
├── infrastructure/repositories/       # Reads your JSON data files
└── presentation/cli/                  # Interactive command-line interface
```

---

## ATS score

After generating, the tool shows a compatibility score (0–100):

| Category           | Max |
|--------------------|-----|
| Contact info       | 10  |
| Document structure | 20  |
| Keyword match      | 30  |
| Experience quality | 20  |
| Skills             | 10  |
| Achievements       | 10  |

Aim for **80+** for best results with automated screening systems.

---

## Dependencies

- [`python-docx`](https://python-docx.readthedocs.io/) — Word document generation
- [`reportlab`](https://www.reportlab.com/) — PDF generation
- [`spacy`](https://spacy.io/) — Keyword extraction from job descriptions
