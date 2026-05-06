from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class PersonalInfo:
    name: str
    title: str
    phone: str
    email: str
    location: str
    linkedin: str = ""
    github: str = ""


@dataclass
class Experience:
    company: str
    position: str
    location: str
    start_date: str
    end_date: str
    description: List[str] = field(default_factory=list)


@dataclass
class Education:
    institution: str
    degree: str
    location: str
    start_date: str
    end_date: str


@dataclass
class Resume:
    personal: PersonalInfo
    summary: str
    experience: List[Experience]
    skills: Dict[str, List[str]]
    education: List[Education]
    certifications: List[Dict] = field(default_factory=list)
    locale: str = "en"
