from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass
class CandidateProfile:
    full_name: str = ""
    email: str = ""
    phone: str = ""
    years_experience: str = ""
    desired_positions: str = ""
    location: str = ""
    tech_stack: List[str] = field(default_factory=list)

    def missing_fields(self) -> List[str]:
        checks = [
            ("full_name", self.full_name),
            ("email", self.email),
            ("phone", self.phone),
            ("years_experience", self.years_experience),
            ("desired_positions", self.desired_positions),
            ("location", self.location),
            ("tech_stack", self.tech_stack),
        ]
        return [field for field, value in checks if not value]

    def to_dict(self) -> Dict[str, str | List[str]]:
        return {
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "years_experience": self.years_experience,
            "desired_positions": self.desired_positions,
            "location": self.location,
            "tech_stack": self.tech_stack,
        }


@dataclass
class ConversationTurn:
    role: str
    content: str


@dataclass
class ConversationState:
    stage: str = "greeting"
    candidate: CandidateProfile = field(default_factory=CandidateProfile)
    turns: List[ConversationTurn] = field(default_factory=list)
    asked_questions: List[str] = field(default_factory=list)
