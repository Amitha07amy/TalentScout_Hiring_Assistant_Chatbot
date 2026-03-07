from hiring_assistant.engine import HiringAssistantEngine
from hiring_assistant.models import ConversationState


def test_end_to_end_flow_without_llm():
    engine = HiringAssistantEngine()
    state = ConversationState()

    inputs = [
        "hello",
        "Amitha R",
        "amitha@example.com",
        "+91 9876543210",
        "2",
        "AI Engineer",
        "Bengaluru",
        "Python, Django",
        "continue",
    ]

    response = ""
    for user in inputs:
        state, response = engine.handle_user_message(state, user)

    assert "screening questions" in response.lower()
    assert "python" in response.lower()
    assert state.stage == "done"
