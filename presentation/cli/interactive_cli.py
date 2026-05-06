import os
from pathlib import Path
from typing import List

from application.use_cases.analyze_keywords import AnalyzeKeywordsUseCase
from application.use_cases.generate_resume import GenerateResumeUseCase
from application.use_cases.score_resume import ScoreResumeUseCase
from domain.value_objects.ats_score import ATSScore

_DEFAULT_OUTPUT_DIR = "/mnt/c/Users/Matheus/Documents/CV-Python"
OUTPUT_DIR = Path(os.environ.get("CV_OUTPUT_DIR", _DEFAULT_OUTPUT_DIR))


class InteractiveCLI:
    def __init__(
        self,
        analyze_keywords: AnalyzeKeywordsUseCase,
        generate_resume: GenerateResumeUseCase,
        score_resume: ScoreResumeUseCase,
    ):
        self._analyze = analyze_keywords
        self._generate = generate_resume
        self._score = score_resume

    def run(self, repository_factory) -> None:
        self._banner()

        repository, lang = self._step_language(repository_factory)
        fmt = self._step_format()
        job_description = self._step_job_description()
        keywords = self._step_analyze_keywords(job_description)

        available_versions = repository.get_available_versions()
        version = self._step_select_version(keywords, available_versions)

        resume = repository.load(version)
        ext = "pdf" if fmt == "pdf" else "docx"
        filename = f"{resume.personal.name.replace(' ', '_')}_Resume_{lang.upper()}.{ext}"
        output_path = str(OUTPUT_DIR / filename)

        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        print(f"\n{'='*70}\nSTEP 5: Resume Generation\n{'-'*70}")
        print(f"Format:  {ext.upper()}")
        print(f"Output:  {output_path}")
        resume_text = self._generate.execute(resume, output_path, fmt)
        print("✓ Resume generated successfully!")

        score = self._step_score(resume, resume_text, keywords)

        self._summary(output_path, version, lang, fmt, score, keywords, resume_text)

    # ── Steps ────────────────────────────────────────────────────────────────

    @staticmethod
    def _step_language(repository_factory):
        print("STEP 0: Language / Idioma")
        print("-" * 70)
        print("  1. English")
        print("  2. Português (PT-BR)")
        choice = input("\nYour choice / Sua escolha (1-2) [default=1]: ").strip()
        lang = "pt" if choice == "2" else "en"
        return repository_factory(lang), lang

    @staticmethod
    def _step_format() -> str:
        print(f"\n{'='*70}\nSTEP 1: Output Format\n{'-'*70}")
        print("  1. DOCX (Word)")
        print("  2. PDF")
        choice = input("\nYour choice (1-2) [default=1]: ").strip()
        return "pdf" if choice == "2" else "docx"

    def _step_job_description(self) -> str:
        print(f"\n{'='*70}\nSTEP 2: Job Description Analysis\n{'-'*70}")
        print("\nHow would you like to provide the job description?")
        print("1. Paste it directly")
        print("2. Load from a text file")
        print("3. Skip (use default resume version)")

        choice = input("\nYour choice (1-3): ").strip()

        if choice == "1":
            print("\nPaste the job description below (Ctrl+D / Ctrl+Z when done):")
            print("-" * 70)
            lines = []
            try:
                while True:
                    lines.append(input())
            except EOFError:
                pass
            return "\n".join(lines)

        if choice == "2":
            path = input("\nEnter the file path: ").strip()
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
                print(f"✓ Loaded from {path}")
                return text
            except OSError as e:
                print(f"✗ Error: {e}")
                return ""

        print("Skipping job description analysis...")
        return ""

    def _step_analyze_keywords(self, job_description: str) -> List[str]:
        if not job_description.strip():
            return []

        print(f"\n{'='*70}\nSTEP 3: Keyword Analysis\n{'-'*70}")
        print("Analyzing job description...")

        keywords = self._analyze.extract(job_description, top_n=30)
        print(f"\n✓ Extracted {len(keywords)} key terms:")
        for i, kw in enumerate(keywords[:15], 1):
            print(f"  {i:2d}. {kw}")
        if len(keywords) > 15:
            print(f"  ... and {len(keywords) - 15} more")

        return keywords

    def _step_select_version(self, keywords: List[str], available_versions: List[str]) -> str:
        print(f"\n{'='*70}\nSTEP 4: Resume Version Selection\n{'-'*70}")

        if not available_versions or len(available_versions) <= 1:
            return available_versions[0] if available_versions else "default"

        suggested = self._analyze.suggest_version(keywords, available_versions) if keywords else "default"

        print("\nAvailable versions:")
        for i, v in enumerate(available_versions, 1):
            marker = " (RECOMMENDED)" if v == suggested else ""
            print(f"  {i}. {v.replace('_', ' ').title()}{marker}")

        choice = input(f"\nSelect (1-{len(available_versions)}) [default=1]: ").strip()
        try:
            idx = int(choice) - 1 if choice else 0
            if 0 <= idx < len(available_versions):
                selected = available_versions[idx]
                print(f"✓ Selected: {selected.replace('_', ' ').title()}")
                return selected
        except ValueError:
            pass

        print("✓ Using default version")
        return "default"

    def _step_score(self, resume, resume_text: str, keywords: List[str]) -> ATSScore:
        print(f"\n{'='*70}\nSTEP 6: ATS Compatibility Analysis\n{'-'*70}")

        match_rate = None
        if keywords:
            match = self._analyze.match(keywords, resume_text)
            match_rate = match.match_rate
            print(f"\nKeyword Match: {match}")
            if match.missing:
                print(f"  Missing: {', '.join(match.missing[:10])}")

        score = self._score.execute(resume, resume_text, match_rate)
        self._print_score(score)
        return score

    # ── Helpers ──────────────────────────────────────────────────────────────

    @staticmethod
    def _banner():
        print(f"\n{'='*70}")
        print(" " * 15 + "ATS-FRIENDLY RESUME BUILDER")
        print("=" * 70)
        print("Generate job-tailored resumes optimized for ATS systems")
        print("=" * 70 + "\n")

    @staticmethod
    def _print_score(score: ATSScore):
        print(f"\n{'='*60}\nATS COMPATIBILITY SCORE\n{'='*60}")
        print(f"\nOverall Score: {score}")
        print(f"Points: {score.points}\n\nFeedback:\n{'-'*60}")
        for item in score.feedback:
            print(f"  {item}")
        print("=" * 60)

    @staticmethod
    def _summary(output_path, version, lang, fmt, score, keywords, resume_text):
        print(f"\n{'='*70}\nSUMMARY\n{'='*70}")
        print(f"File:    {output_path}")
        print(f"Lang:    {'PT-BR' if lang == 'pt' else 'English'}")
        print(f"Format:  {fmt.upper()}")
        print(f"Version: {version.replace('_', ' ').title()}")
        print(f"Score:   {score}")
        if keywords:
            matched = sum(1 for k in keywords if k.lower() in resume_text.lower())
            print(f"Keywords matched: {matched}/{len(keywords)}")
        print("=" * 70)
        print(f"\n✓ Done! File saved to:\n  {output_path}\n")
