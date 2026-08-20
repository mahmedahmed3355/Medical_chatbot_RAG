from unittest.mock import Mock, patch

import pytest

from app.common.custom_exception import CustomException
from app.components.data_loader import process_and_store_pdfs


@patch("app.components.data_loader.save_vector_store")
@patch("app.components.data_loader.create_text_chunks")
@patch("app.components.data_loader.load_pdf_files")
def test_process_and_store_pdfs_success(
    mock_load_pdfs,
    mock_create_chunks,
    mock_save_vector_store,
):
    documents = [Mock()]
    chunks = [Mock(), Mock()]
    vector_store = Mock()

    mock_load_pdfs.return_value = documents
    mock_create_chunks.return_value = chunks
    mock_save_vector_store.return_value = vector_store

    result = process_and_store_pdfs()

    assert result is vector_store

    mock_create_chunks.assert_called_once_with(
        documents
    )

    mock_save_vector_store.assert_called_once_with(
        chunks
    )


@patch("app.components.data_loader.load_pdf_files")
def test_process_and_store_pdfs_failure(
    mock_load_pdfs,
):
    mock_load_pdfs.side_effect = RuntimeError(
        "PDF failure"
    )

    with pytest.raises(
        CustomException,
        match="Failed to process and store PDFs",
    ):
        process_and_store_pdfs()
