from app.services import chat_service


def test_answer_question_returns_qa_chain_result(
    monkeypatch,
):
    captured = {}

    class FakeChain:
        def invoke(self, payload):
            captured["payload"] = payload
            return {
                "result": "Diabetes is a chronic condition.",
            }

    monkeypatch.setattr(
        chat_service,
        "create_qa_chain",
        lambda: FakeChain(),
    )

    result = chat_service.answer_question(
        "What is diabetes?",
    )

    assert result == "Diabetes is a chronic condition."

    assert captured["payload"] == {
        "query": "What is diabetes?",
    }


def test_answer_question_returns_fallback_when_result_missing(
    monkeypatch,
):
    class FakeChain:
        def invoke(self, payload):
            return {}

    monkeypatch.setattr(
        chat_service,
        "create_qa_chain",
        lambda: FakeChain(),
    )

    result = chat_service.answer_question(
        "What is diabetes?",
    )

    assert result == "No response"
