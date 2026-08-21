from unittest.mock import MagicMock, patch

from app.application import app


def test_internal_exception_returns_safe_error_and_request_id():
    app.config.update(
        TESTING=True,
        SECRET_KEY="test-secret-key",
    )

    fake_chain = MagicMock()
    fake_chain.invoke.side_effect = RuntimeError(
        "super-secret-internal-error"
    )

    with patch(
        "app.components.retriever.create_qa_chain",
        return_value=fake_chain,
    ):
        with app.test_client() as client:
            response = client.post(
                "/",
                data={"prompt": "test medical question"},
            )

    assert response.status_code == 500

    body = response.get_data(as_text=True)

    assert (
        "Something went wrong while processing your request."
        in body
    )

    assert "super-secret-internal-error" not in body

    assert "X-Request-ID" in response.headers
    assert response.headers["X-Request-ID"]
