from unittest.mock import Mock, patch

import pytest

from app.common.custom_exception import CustomException
from app.components.vector_store import (
    load_vector_store,
    save_vector_store,
)


def test_load_vector_store_missing_path(tmp_path):
    missing_path = tmp_path / "missing"

    with pytest.raises(
        CustomException,
        match="Failed to load vector store",
    ):
        load_vector_store(missing_path)


@patch("app.components.vector_store.FAISS")
@patch(
    "app.components.vector_store.get_embedding_model"
)
def test_load_vector_store_success(
    mock_get_embedding_model,
    mock_faiss,
    tmp_path,
):
    embedding_model = Mock()
    vector_store = Mock()

    mock_get_embedding_model.return_value = embedding_model
    mock_faiss.load_local.return_value = vector_store

    db_path = tmp_path / "db"
    db_path.mkdir()

    result = load_vector_store(db_path)

    assert result is vector_store

    mock_faiss.load_local.assert_called_once_with(
        str(db_path),
        embedding_model,
        allow_dangerous_deserialization=True,
    )


@patch("app.components.vector_store.FAISS")
@patch(
    "app.components.vector_store.get_embedding_model"
)
def test_save_vector_store_success(
    mock_get_embedding_model,
    mock_faiss,
    tmp_path,
):
    embedding_model = Mock()
    vector_store = Mock()

    mock_get_embedding_model.return_value = embedding_model
    mock_faiss.from_documents.return_value = vector_store

    db_path = tmp_path / "db"
    chunks = [Mock(), Mock()]

    result = save_vector_store(
        chunks,
        db_path,
    )

    assert result is vector_store

    vector_store.save_local.assert_called_once_with(
        str(db_path)
    )


def test_save_vector_store_empty_chunks(tmp_path):
    with pytest.raises(
        CustomException,
        match="Failed to save vector store",
    ):
        save_vector_store(
            [],
            tmp_path / "db",
        )
