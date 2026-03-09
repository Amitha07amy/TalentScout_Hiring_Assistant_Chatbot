from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Optional

from hiring_assistant.models import CandidateProfile


class CandidateStore:
    def __init__(self, base_dir: str = "data") -> None:
        self.base_path = Path(base_dir)
        self.base_path.mkdir(parents=True, exist_ok=True)
        self.path = self.base_path / "candidate_submissions.jsonl"
        self._sheet = self._init_google_sheet()

    @staticmethod
    def _hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    def _init_google_sheet(self) -> Optional[object]:
        spreadsheet_id = os.getenv("GOOGLE_SHEETS_SPREADSHEET_ID", "").strip()
        service_account_json = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON", "").strip()
        worksheet_name = os.getenv("GOOGLE_SHEETS_WORKSHEET_NAME", "candidate_submissions").strip()

        if not spreadsheet_id or not service_account_json:
            return None

        try:
            import gspread
            from gspread.exceptions import WorksheetNotFound
            from google.oauth2.service_account import Credentials

            credentials_info = json.loads(service_account_json)
            scopes = ["https://www.googleapis.com/auth/spreadsheets"]
            credentials = Credentials.from_service_account_info(credentials_info, scopes=scopes)
            client = gspread.authorize(credentials)
            workbook = client.open_by_key(spreadsheet_id)

            try:
                sheet = workbook.worksheet(worksheet_name)
            except WorksheetNotFound:
                sheet = workbook.add_worksheet(title=worksheet_name, rows=1000, cols=20)

            if not sheet.get_all_values():
                sheet.append_row(
                    [
                        "timestamp_utc",
                        "full_name",
                        "email_hash",
                        "phone_hash",
                        "years_experience",
                        "desired_positions",
                        "location",
                        "tech_stack",
                        "metadata_json",
                    ],
                    value_input_option="RAW",
                )
            return sheet
        except Exception:
            return None

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

    def _append_to_local_jsonl(self, record: Dict[str, object]) -> None:
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=True) + "\n")

    def _append_to_google_sheet(self, record: Dict[str, object]) -> None:
        if self._sheet is None:
            raise RuntimeError("Google Sheet is not configured.")

        candidate = record["candidate"]
        metadata = record["metadata"]
        self._sheet.append_row(
            [
                record["timestamp_utc"],
                candidate["full_name"],
                candidate["email_hash"],
                candidate["phone_hash"],
                candidate["years_experience"],
                candidate["desired_positions"],
                candidate["location"],
                ", ".join(candidate["tech_stack"]),
                json.dumps(metadata, ensure_ascii=True),
            ],
            value_input_option="RAW",
        )

    def append_submission(self, candidate: CandidateProfile, metadata: Dict[str, str]) -> None:
        record = self._redacted_record(candidate, metadata)
        if self._sheet is not None:
            try:
                self._append_to_google_sheet(record)
                return
            except Exception:
                pass
        self._append_to_local_jsonl(record)
