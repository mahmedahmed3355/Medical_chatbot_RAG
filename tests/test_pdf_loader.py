from unittest.mock import Mock, patch

import pytest

from app.common.custom_exception import CustomException
from app.components.pdf_loader import (
    create_text_chunks,
    load_pdf_files,
)


def test_load_pdf_files_missing_directory(tmp_path):
    missing_path = tmp_path / "missing"

    with pytest.raises(
        CustomException,
        match="Failed to load PDF files",
    ):
        load_pdf_files(missing_path)


@patch("app.components.pdf_loader.DirectoryLoader")
def test_load_pdf_files_success(mock_loader, tmp_path):
    mock_documents = [Mock(), Mock()]

    loader_instance = mock_loader.return_value
    loader_instance.load.return_value = mock_documents

    result = load_pdf_files(tmp_path)

    assert result == mock_documents

    mock_loader.assert_called_once()


@patch("app.components.pdf_loader.RecursiveCharacterTextSplitter")
def test_create_text_chunks_success(mock_splitter):
    documents = [Mock(), Mock()]
    chunks = [Mock(), Mock(), Mock()]

    splitter_instance = mock_splitter.return_value
    splitter_instance.split_documents.return_value = chunks

    result = create_text_chunks(documents)

    assert result == chunks

    splitter_instance.split_documents.assert_called_once_with(documents)


def test_create_text_chunks_empty_documents():
    with pytest.raises(
        CustomException,
        match="Failed to create text chunks",
    ):
        create_text_chunks([])


@patch("app.components.pdf_loader.DirectoryLoader")
def test_load_pdf_files_rejects_empty_loader_result(
    mock_loader,
    tmp_path,
):
    loader_instance = mock_loader.return_value
    loader_instance.load.return_value = []

    with pytest.raises(
        CustomException,
        match="Failed to load PDF files",
    ):
        load_pdf_files(tmp_path)


@patch("app.components.pdf_loader.RecursiveCharacterTextSplitter")
def test_create_text_chunks_rejects_empty_split_result(
    mock_splitter,
):
    documents = [Mock()]

    splitter_instance = mock_splitter.return_value
    splitter_instance.split_documents.return_value = []

    with pytest.raises(
        CustomException,
        match="Failed to create text chunks",
    ):
        create_text_chunks(documents)


@patch("app.components.pdf_loader.RecursiveCharacterTextSplitter")
def test_create_text_chunks_reraises_custom_exception(
    mock_splitter,
):
    documents = [Mock()]
    error = CustomException("Known chunk failure")

    splitter_instance = mock_splitter.return_value
    splitter_instance.split_documents.side_effect = error

    with pytest.raises(CustomException) as exc_info:
        create_text_chunks(documents)

    assert exc_info.value is error


@patch("app.components.pdf_loader.DirectoryLoader")
def test_load_pdf_files_reraises_custom_exception(
    mock_loader,
    tmp_path,
):
    error = CustomException("Known loader failure")

    loader_instance = mock_loader.return_value
    loader_instance.load.side_effect = error

    with pytest.raises(CustomException) as exc_info:
        load_pdf_files(tmp_path)

    assert exc_info.value is error
