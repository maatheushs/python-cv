import re
from collections import Counter
from typing import List

from domain.value_objects.keyword_match import KeywordMatch

STOP_WORDS = {
    'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
    'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'be', 'been',
    'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
    'should', 'could', 'may', 'might', 'must', 'can', 'this', 'that',
    'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
    'what', 'which', 'who', 'when', 'where', 'why', 'how', 'all', 'each',
    'every', 'both', 'few', 'more', 'most', 'other', 'some', 'such',
}

TECH_KEYWORDS = {
    'javascript', 'typescript', 'python', 'java', 'go', 'rust', 'php',
    'node', 'react', 'vue', 'angular', 'nestjs', 'express', 'django',
    'flask', 'spring', 'docker', 'kubernetes', 'aws', 'azure', 'gcp',
    'postgresql', 'mysql', 'mongodb', 'redis', 'graphql', 'rest', 'api',
    'microservices', 'serverless', 'lambda', 'ec2', 's3', 'sqs', 'sns',
    'git', 'ci/cd', 'jenkins', 'github', 'gitlab', 'jira', 'agile',
    'scrum', 'tdd', 'bdd', 'jest', 'pytest', 'junit', 'selenium',
    'terraform', 'ansible', 'grafana', 'prometheus', 'cloudwatch',
    'datadog', 'elk', 'kafka', 'rabbitmq', 'nginx', 'apache',
}


def extract_keywords(job_description: str, top_n: int = 30) -> List[str]:
    text = re.sub(r'[^a-z0-9\s\-/]', ' ', job_description.lower())
    words = [w for w in text.split() if w not in STOP_WORDS and len(w) > 2]
    bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]

    word_freq = Counter(words)
    bigram_freq = Counter(bigrams)

    for word in word_freq:
        if word in TECH_KEYWORDS:
            word_freq[word] *= 3

    for bigram in bigram_freq:
        if any(tech in bigram for tech in TECH_KEYWORDS):
            bigram_freq[bigram] *= 2

    all_keywords = (
        [w for w, _ in word_freq.most_common(top_n)]
        + [b for b, _ in bigram_freq.most_common(top_n // 2)]
    )

    seen: set = set()
    unique = []
    for kw in all_keywords:
        if kw not in seen:
            seen.add(kw)
            unique.append(kw)

    return unique[:top_n]


def match_keywords(keywords: List[str], resume_text: str) -> KeywordMatch:
    resume_lower = resume_text.lower()
    matched = [kw for kw in keywords if kw.lower() in resume_lower]
    missing = [kw for kw in keywords if kw.lower() not in resume_lower]
    rate = round(len(matched) / len(keywords) * 100, 1) if keywords else 0.0
    return KeywordMatch(matched=matched, missing=missing, match_rate=rate, total_keywords=len(keywords))


def suggest_version(keywords: List[str], available_versions: List[str]) -> str:
    text = ' '.join(k.lower() for k in keywords)

    if any(w in text for w in ('backend', 'api', 'microservices', 'architecture')):
        if 'backend_focused' in available_versions:
            return 'backend_focused'

    if any(w in text for w in ('frontend', 'react', 'full-stack', 'fullstack')):
        if 'full_stack' in available_versions:
            return 'full_stack'

    if any(w in text for w in ('lead', 'senior', 'mentor', 'team')):
        if 'leadership' in available_versions:
            return 'leadership'

    return 'default'
