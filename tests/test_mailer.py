from hiring_assistant.mailer import _build_email_body, is_email_delivery_enabled
from hiring_assistant.models import CandidateProfile


def test_email_delivery_flag_without_smtp(monkeypatch):
    for key in ["SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "MAIL_FROM"]:
        monkeypatch.delenv(key, raising=False)
    assert not is_email_delivery_enabled()


def test_build_email_body_contains_reply_instruction():
    candidate = CandidateProfile(full_name="Amitha", email="a@example.com")
    body = _build_email_body(candidate, {"Python": ["Q1", "Q2", "Q3"]})
    assert "Please reply to this email" in body
    assert "1. Q1" in body
