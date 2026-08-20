from unittest.mock import patch

import pytest

from app.common.custom_exception import CustomException
from app.components.embeddings import get_embedding_model


@patch("app.components.embeddings.HuggingFaceEmbeddings")
def test_get_embedding_model_success(mock_embeddings):
    model = object()
    mock_embeddings.return_value = model

    result = get_embedding_model()

    assert result is model

    mock_embeddings.assert_called_once_with(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
    )


@patch("app.components.embeddings.HuggingFaceEmbeddings")
def test_get_embedding_model_failure(mock_embeddings):
    mock_embeddings.side_effect = RuntimeError("model failure")

    with pytest.raises(
        CustomException,
        match="Failed to load embedding model",
    ):
        get_embedding_model()
