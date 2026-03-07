# TalentScout Hiring Assistant Chatbot

A Streamlit-based AI/ML internship assignment project that implements an intelligent hiring assistant for initial candidate screening.

The chatbot:
- Greets candidates and explains purpose.
- Collects required profile details.
- Accepts declared tech stack.
- Generates 3-5 technical screening questions per technology.
- Maintains coherent, context-aware conversation flow.
- Handles fallback and conversation-ending intents.
- Emails screening questions to the candidate (SMTP), so they can reply on email.
- Stores simulated/anonymized submission records.

## 1. Project Overview

This project is designed for the fictional recruitment agency **TalentScout** to streamline initial technical screening before human interviewer rounds.

Core objective: build a prompt-driven assistant that gathers candidate information and generates tailored technical questions based on the candidate's tech stack.

## 2. Features Implemented

- `Streamlit` chat interface with clear, focused UX.
- Conversation state machine for robust context handling.
- Required fields captured:
  - Full Name
  - Email Address
  - Phone Number
  - Years of Experience
  - Desired Position(s)
  - Current Location
  - Tech Stack
- Exit keywords: `exit`, `quit`, `bye`, `goodbye`, `end`, `stop`.
- Technical question generation:
  - Primary: OpenAI model via API key.
  - Fallback: curated deterministic question bank.
  - Role-aware focus: prioritizes the most relevant technologies (up to 5) and asks 3 questions per selected technology.
- Email delivery:
  - Sends screening questions to candidate email via SMTP.
  - Candidate can reply directly to the same email thread.
- Fallback mechanism for invalid/unexpected user inputs.
- Graceful conversation closure with next-step messaging.
- Simulated secure data handling:
  - `email` and `phone` are stored as SHA-256 hashes in JSONL.

## 3. Tech Stack

- Python 3.10+
- Streamlit
- OpenAI Python SDK
- python-dotenv
- pytest

## 4. Installation

From `/Users/amitha/AI_ML_Intern_assignment`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

(Optional) configure environment:

```bash
cp .env.example .env
# Add OPENAI_API_KEY in .env to enable LLM-powered question generation
# Add SMTP_* and MAIL_* fields to send screening questions over email
```

## 5. Run The App

```bash
streamlit run app.py
```

Then open the local URL displayed by Streamlit.

## 6. Usage Guide

1. Start chat and send any message to initiate screening.
2. Provide requested details step-by-step.
3. Enter tech stack as comma-separated list (example: `Python, Django, PostgreSQL, AWS`).
4. Receive generated technical screening questions grouped by technology.
5. If SMTP is configured, questions are emailed to candidate and they should reply to that email.
6. Type `exit` anytime to stop.

## 6.1 SMTP Setup Example (Gmail)

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USE_SSL=false
SMTP_TIMEOUT_SECONDS=30
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_REPLY_TO=your-email@gmail.com
```

Use an app password (not your normal account password).

Alternative SSL mode:

```bash
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USE_SSL=true
SMTP_TIMEOUT_SECONDS=30
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
MAIL_FROM=your-email@gmail.com
MAIL_REPLY_TO=your-email@gmail.com
```

## 7. Prompt Design

### System Prompt Strategy
The system prompt constrains behavior to hiring-screening scope and enforces safe behavior:
- Stay on task (candidate screening only).
- Keep responses concise.
- Redirect unrelated prompts.
- Avoid collecting highly sensitive secrets.

### Question Generation Prompt Strategy
A structured user prompt injects candidate profile fields and requests strict JSON output:
- Includes candidate context (experience, desired role, location, stack).
- Requires practical questions with varied difficulty.
- Enforces parseable schema:
  - `questions_by_tech: { tech_name: [questions...] }`

## 8. Architecture & Code Structure

```text
app.py
hiring_assistant/
  __init__.py
  engine.py          # conversation orchestration and flow
  llm.py             # LLM integration + JSON parsing + fallback
  mailer.py          # SMTP email sender for screening questions
  models.py          # dataclasses for candidate and conversation state
  prompts.py         # reusable prompt templates
  question_bank.py   # deterministic fallback technical questions
  storage.py         # anonymized simulated persistence (JSONL)
  validators.py      # validation + exit detection + tech parsing
tests/
  test_engine.py
  test_validators.py
```

## 9. Data Privacy & Handling

- Uses simulated local storage only (`data/candidate_submissions.jsonl`).
- Contact information is not stored raw in records; email and phone are hashed.
- Keep `.env` private and never commit API keys.
- In real deployments, add encryption at rest, access controls, retention rules, and explicit consent flow for GDPR compliance.

## 10. Challenges & Solutions

- **Challenge:** LLM output can be unstructured.
  - **Solution:** enforce strict JSON schema in prompt + parser + fallback question bank.
- **Challenge:** users can provide malformed contact details.
  - **Solution:** field-level validators with guided retry prompts.
- **Challenge:** requirement to avoid drift from purpose.
  - **Solution:** scoped system prompt and deterministic fallback responses.

## 11. Testing

Run tests:

```bash
pytest -q
```

## 12. Submission Checklist

- Source code available in repository.
- README with setup, usage, architecture, prompt design, and challenges.
- Local demo ready via Streamlit.
- Optional: attach Loom walkthrough or cloud deployment link.

## 13. Optional Enhancement Ideas

- Multilingual support.
- Sentiment analysis during interaction.
- Candidate-specific personalization using previous interaction history.
- Deploy on Streamlit Community Cloud for live demo.