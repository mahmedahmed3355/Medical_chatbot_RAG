from unittest.mock import patch

import pytest

from app.application import app


@pytest.fixture()
def client():
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
    )

    with app.test_client() as test_client:
        yield test_client


def test_index_get_returns_success(client):
    response = client.get("/")

    assert response.status_code == 200


def test_index_post_empty_prompt_returns_validation_error(client):
    response = client.post(
        "/",
        data={"prompt": "   "},
        follow_redirects=False,
    )

    assert response.status_code == 400


def test_index_post_successfully_runs_rag_chain(client):
    class FakeQAChain:
        def invoke(self, payload):
            assert payload == {
                "query": "What is diabetes?"
            }

            return {
                "result": "Diabetes is a chronic medical condition."
            }

    with patch(
        "app.application.answer_question",
        return_value="Diabetes is a chronic medical condition.",
    ):
        response = client.post(
            "/",
            data={"prompt": "What is diabetes?"},
            follow_redirects=False,
        )

    assert response.status_code == 302

    with client.session_transaction() as session:
        messages = session["messages"]

    assert len(messages) == 2

    assert messages[0] == {
        "role": "user",
        "content": "What is diabetes?",
    }

    assert messages[1] == {
        "role": "assistant",
        "content": "Diabetes is a chronic medical condition.",
    }


def test_index_post_handles_rag_failure(client):
    with patch(
        "app.application.answer_question",
        side_effect=RuntimeError("RAG service unavailable"),
    ):
        response = client.post(
            "/",
            data={"prompt": "Test medical question"},
        )

    assert response.status_code == 500
    assert (
        b"Something went wrong while processing your request."
        in response.data
    )
    assert b"RAG service unavailable" not in response.data
    assert response.headers.get("X-Request-ID")


def test_clear_removes_chat_messages(client):
    with client.session_transaction() as session:
        session["messages"] = [
            {
                "role": "user",
                "content": "Hello",
            }
        ]

    response = client.get(
        "/clear",
        follow_redirects=False,
    )

    assert response.status_code == 302

    with client.session_transaction() as session:
        assert "messages" not in session


def test_clear_without_existing_messages(client):
    response = client.get(
        "/clear",
        follow_redirects=False,
    )

    assert response.status_code == 302


def test_nl2br_converts_newlines():
    from app.application import nl2br

    result = nl2br("line one\nline two")

    assert str(result) == "line one<br>\nline two"


def test_post_empty_prompt_returns_validation_error():
    client = app.test_client()

    response = client.post(
        "/",
        data={"prompt": "   "},
    )

    assert response.status_code == 400


def test_post_prompt_over_2000_characters_returns_validation_error():
    client = app.test_client()

    response = client.post(
        "/",
        data={"prompt": "a" * 2001},
    )

    assert response.status_code == 400
