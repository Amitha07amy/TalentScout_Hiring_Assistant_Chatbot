from __future__ import annotations

from typing import List, Tuple

from hiring_assistant.llm import generate_questions
from hiring_assistant.mailer import format_email_error, is_email_delivery_enabled, send_screening_questions
from hiring_assistant.models import ConversationState, ConversationTurn
from hiring_assistant.storage import CandidateStore
from hiring_assistant.validators import (
    is_exit_intent,
    parse_tech_stack,
    valid_email,
    valid_experience,
    valid_phone,
)

EXIT_MESSAGE = (
    "Thanks for your time. We have ended this screening chat. "
    "TalentScout will review your profile and reach out with next steps."
)


class HiringAssistantEngine:
    def __init__(self) -> None:
        self.store = CandidateStore(base_dir="data")

    @staticmethod
    def intro_message() -> str:
        return (
            "Hello, I am TalentScout's Hiring Assistant. "
            "I will collect your basic profile details and then generate technical "
            "screening questions based on your tech stack.\n\n"
            "You can type `exit` anytime to end the conversation.\n\n"
            "Let's begin. Please share your full name."
        )

    @staticmethod
    def _field_prompt(stage: str) -> str:
        prompts = {
            "collect_name": "Please share your full name.",
            "collect_email": "Please provide your email address.",
            "collect_phone": "Please provide your phone number (include country code if applicable).",
            "collect_experience": "How many years of professional experience do you have?",
            "collect_position": "What role(s) are you interested in?",
            "collect_location": "What is your current location?",
            "collect_stack": "List your tech stack separated by commas (languages, frameworks, databases, tools).",
        }
        return prompts.get(stage, "Please continue.")

    def _next_stage(self, stage: str) -> str:
        order = [
            "collect_name",
            "collect_email",
            "collect_phone",
            "collect_experience",
            "collect_position",
            "collect_location",
            "collect_stack",
            "generate_questions",
            "done",
        ]
        idx = order.index(stage)
        return order[min(idx + 1, len(order) - 1)]

    @staticmethod
    def _format_questions(questions_by_tech: dict[str, List[str]]) -> str:
        lines = ["Thank you. Based on your tech stack, here are your screening questions:"]
        for tech, questions in questions_by_tech.items():
            lines.append(f"\n{tech}:")
            for i, q in enumerate(questions[:5], start=1):
                lines.append(f"{i}. {q}")
        lines.append(
            "\nThis concludes the initial screening. TalentScout will contact you about the next steps."
        )
        return "\n".join(lines)

    def _handle_collection(self, state: ConversationState, user_text: str) -> Tuple[ConversationState, str]:
        stage = state.stage
        candidate = state.candidate

        if stage == "collect_name":
            candidate.full_name = user_text.strip()
            state.stage = self._next_stage(stage)
            return state, self._field_prompt(state.stage)

        if stage == "collect_email":
            if not valid_email(user_text):
                return state, "That doesn't look like a valid email. Please enter a valid email address."
            candidate.email = user_text.strip()
            state.stage = self._next_stage(stage)
            return state, self._field_prompt(state.stage)

        if stage == "collect_phone":
            if not valid_phone(user_text):
                return state, "That phone number format seems invalid. Please provide a valid phone number."
            candidate.phone = user_text.strip()
            state.stage = self._next_stage(stage)
            return state, self._field_prompt(state.stage)

        if stage == "collect_experience":
            if not valid_experience(user_text):
                return state, "Please enter years of experience as a number (for example: 3 or 4.5)."
            candidate.years_experience = user_text.strip()
            state.stage = self._next_stage(stage)
            return state, self._field_prompt(state.stage)

        if stage == "collect_position":
            candidate.desired_positions = user_text.strip()
            state.stage = self._next_stage(stage)
            return state, self._field_prompt(state.stage)

        if stage == "collect_location":
            candidate.location = user_text.strip()
            state.stage = self._next_stage(stage)
            return state, self._field_prompt(state.stage)

        if stage == "collect_stack":
            stack = parse_tech_stack(user_text)
            if not stack:
                return state, "Please provide at least one technology, separated by commas."
            candidate.tech_stack = stack
            state.stage = self._next_stage(stage)
            return state, "Generating your technical screening questions now..."

        return state, "Please continue."

    def handle_user_message(self, state: ConversationState, user_text: str) -> Tuple[ConversationState, str]:
        text = user_text.strip()
        state.turns.append(ConversationTurn(role="user", content=text))

        if is_exit_intent(text):
            state.stage = "done"
            state.turns.append(ConversationTurn(role="assistant", content=EXIT_MESSAGE))
            return state, EXIT_MESSAGE

        if state.stage == "greeting":
            state.stage = "collect_name"
            msg = self.intro_message()
            state.turns.append(ConversationTurn(role="assistant", content=msg))
            return state, msg

        if state.stage.startswith("collect_"):
            state, response = self._handle_collection(state, text)
            state.turns.append(ConversationTurn(role="assistant", content=response))
            return state, response

        if state.stage == "generate_questions":
            questions = generate_questions(state.candidate)
            state.asked_questions = [q for qs in questions.values() for q in qs]
            local_preview = self._format_questions(questions)
            if is_email_delivery_enabled():
                try:
                    email_status = send_screening_questions(state.candidate, questions)
                    response = (
                        f"{email_status}\n\n"
                        "Please check your inbox and reply directly to that email with your answers.\n\n"
                        f"Preview:\n\n{local_preview}"
                    )
                except Exception as exc:
                    reason = format_email_error(exc)
                    response = (
                        "I could not send email due to SMTP delivery failure. "
                        f"Reason: {reason}. "
                        "Sharing your questions here instead.\n\n"
                        f"{local_preview}"
                    )
            else:
                response = (
                    "Email delivery is not configured yet. "
                    "Sharing your questions here instead.\n\n"
                    f"{local_preview}"
                )
            self.store.append_submission(
                candidate=state.candidate,
                metadata={"status": "screening_completed", "questions_count": str(len(state.asked_questions))},
            )
            state.stage = "done"
            state.turns.append(ConversationTurn(role="assistant", content=response))
            return state, response

        if state.stage == "done":
            response = (
                "This chat has already concluded. "
                "If you want to restart, click the 'Start New Conversation' button."
            )
            state.turns.append(ConversationTurn(role="assistant", content=response))
            return state, response

        fallback = (
            "I can help only with TalentScout's hiring screening flow. "
            "Please provide the requested candidate details or type `exit` to finish."
        )
        state.turns.append(ConversationTurn(role="assistant", content=fallback))
        return state, fallback
