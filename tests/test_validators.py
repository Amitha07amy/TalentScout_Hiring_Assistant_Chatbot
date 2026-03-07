from hiring_assistant.validators import (
    is_exit_intent,
    parse_tech_stack,
    valid_email,
    valid_experience,
    valid_phone,
)


def test_valid_email():
    assert valid_email("candidate@example.com")
    assert not valid_email("candidate@com")


def test_valid_phone():
    assert valid_phone("+1 555 123 4567")
    assert not valid_phone("abc123")


def test_valid_experience():
    assert valid_experience("3")
    assert valid_experience("4.5 years")
    assert not valid_experience("many")


def test_parse_tech_stack_dedup():
    assert parse_tech_stack("Python, Django, python,  ,SQL") == ["Python", "Django", "SQL"]


def test_parse_tech_stack_with_categories_and_levels():
    stack = parse_tech_stack("Programming : Python, AWS (basic), AI/ML : PyTorch, python")
    assert stack == ["Python", "AWS", "PyTorch"]


def test_exit_intent():
    assert is_exit_intent("exit")
    assert is_exit_intent("I want to quit now")
