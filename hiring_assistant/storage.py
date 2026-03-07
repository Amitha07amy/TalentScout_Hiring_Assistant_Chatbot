from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict

from hiring_assistant.models import CandidateProfile


class CandidateStore:
    def __init__(self, base_dir: str = "data") -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.path = self.base_path / "candidate_submissions.jsonl"

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _redacted_record(self, candidate: CandidateProfile, metadata: Dict[str, str]) -> Dict[str, object]:
        return {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "candidate": {
                "full_name": candidate.full_name,
                "email_hash": self._hash(candidate.email.lower().strip()),
                "phone_hash": self._hash(candidate.phone.strip()),
                "years_experience": candidate.years_experience,
                "desired_positions": candidate.desired_positions,
                "location": candidate.location,
                "tech_stack": candidate.tech_stack,
            },
            "metadata": metadata,
        }

    def append_submission(self, candidate: CandidateProfile, metadata: Dict[str, str]) -> None:
        record = self._redacted_record(candidate, metadata)
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=True) + "\n")
