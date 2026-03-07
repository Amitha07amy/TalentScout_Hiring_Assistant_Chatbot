from hiring_assistant.llm import _bucket_for_tech, _select_relevant_tech_stack
from hiring_assistant.models import CandidateProfile
from hiring_assistant.question_bank import DEFAULT_GENERIC_QUESTIONS, questions_for_tech


def test_random_selection_caps_and_covers_multiple_areas():
    candidate = CandidateProfile(
        desired_positions="AI Engineer",
        tech_stack=[
            "Tableau",
            "PowerBI",
            "Python",
            "OpenAI API",
            "LangChain",
            "Docker",
            "SQL",
            "PyTorch",
        ],
    )

    selected = _select_relevant_tech_stack(candidate)

    assert len(selected) == 5
    assert set(selected).issubset(set(candidate.tech_stack))
    selected_buckets = {_bucket_for_tech(tech) for tech in selected}
    assert len(selected_buckets) >= 2


def test_question_bank_role_coverage():
    assert questions_for_tech("DevOps") != DEFAULT_GENERIC_QUESTIONS
    assert questions_for_tech("MLOps") != DEFAULT_GENERIC_QUESTIONS
    assert questions_for_tech("SDE") != DEFAULT_GENERIC_QUESTIONS
    assert questions_for_tech("Video Editing") != DEFAULT_GENERIC_QUESTIONS
    assert questions_for_tech("Web Designing") != DEFAULT_GENERIC_QUESTIONS
    assert questions_for_tech("Testing") != DEFAULT_GENERIC_QUESTIONS
    assert questions_for_tech("Research") != DEFAULT_GENERIC_QUESTIONS
