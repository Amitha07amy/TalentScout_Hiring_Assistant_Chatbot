from __future__ import annotations

import os
import smtplib
from email.message import EmailMessage
from typing import Dict, List, Tuple

from hiring_assistant.models import CandidateProfile


def _smtp_configured() -> bool:
    required = ["SMTP_HOST", "SMTP_PORT", "SMTP_USERNAME", "SMTP_PASSWORD", "MAIL_FROM"]
    return all(os.getenv(k, "").strip() for k in required)


def is_email_delivery_enabled() -> bool:
    return _smtp_configured()


def format_email_error(exc: Exception) -> str:
    return f"{exc.__class__.__name__}: {str(exc).strip() or 'unknown error'}"


def _build_email_body(candidate: CandidateProfile, questions_by_tech: Dict[str, List[str]]) -> str:
    lines: List[str] = []
    lines.append(f"Hi {candidate.full_name},")
    lines.append("")
    lines.append("Thank you for applying with TalentScout.")
    lines.append("Please reply to this email with your answers to the screening questions below.")
    lines.append("")

    q_no = 1
    for tech, questions in questions_by_tech.items():
        lines.append(f"{tech}:")
        for question in questions:
            lines.append(f"{q_no}. {question}")
            q_no += 1
        lines.append("")

    lines.append("Reply format suggestion:")
    lines.append("1) <your answer>")
    lines.append("2) <your answer>")
    lines.append("...")
    lines.append("")
    lines.append("Best regards,")
    lines.append("TalentScout Hiring Team")
    return "\n".join(lines)


def _send_with_mode(
    message: EmailMessage,
    smtp_host: str,
    smtp_port: int,
    smtp_user: str,
    smtp_password: str,
    smtp_use_ssl: bool,
    timeout_seconds: int,
) -> None:
    if smtp_use_ssl:
        with smtplib.SMTP_SSL(smtp_host, smtp_port, timeout=timeout_seconds) as server:
            server.login(smtp_user, smtp_password)
            server.send_message(message)
    else:
        with smtplib.SMTP(smtp_host, smtp_port, timeout=timeout_seconds) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(message)


def send_screening_questions(candidate: CandidateProfile, questions_by_tech: Dict[str, List[str]]) -> str:
    if not is_email_delivery_enabled():
        raise RuntimeError("SMTP is not configured")

    smtp_host = os.getenv("SMTP_HOST", "").strip()
    smtp_port = int(os.getenv("SMTP_PORT", "587").strip())
    smtp_user = os.getenv("SMTP_USERNAME", "").strip()
    smtp_password = os.getenv("SMTP_PASSWORD", "").strip()
    smtp_use_ssl = os.getenv("SMTP_USE_SSL", "false").strip().lower() in {"1", "true", "yes"}
    smtp_timeout = int(os.getenv("SMTP_TIMEOUT_SECONDS", "30").strip())
    mail_from = os.getenv("MAIL_FROM", "").strip()
    reply_to = os.getenv("MAIL_REPLY_TO", mail_from).strip()

    message = EmailMessage()
    message["Subject"] = "TalentScout Screening Questions - Please Reply"
    message["From"] = mail_from
    message["To"] = candidate.email
    message["Reply-To"] = reply_to
    message.set_content(_build_email_body(candidate, questions_by_tech))

    attempts: List[Tuple[int, bool]] = [(smtp_port, smtp_use_ssl)]
    # Gmail fallback: auto-try the alternate secure mode if initial attempt times out/fails.
    if smtp_host.lower() == "smtp.gmail.com":
        alt = (465, True) if (smtp_port, smtp_use_ssl) != (465, True) else (587, False)
        attempts.append(alt)

    last_error: Exception | None = None
    for port, use_ssl in attempts:
        try:
            _send_with_mode(
                message=message,
                smtp_host=smtp_host,
                smtp_port=port,
                smtp_user=smtp_user,
                smtp_password=smtp_password,
                smtp_use_ssl=use_ssl,
                timeout_seconds=smtp_timeout,
            )
            return f"Questions emailed to {candidate.email}. Please reply to that email with your answers."
        except Exception as exc:
            last_error = exc

    if last_error is not None:
        raise last_error

    raise RuntimeError("SMTP send failed for unknown reason")
