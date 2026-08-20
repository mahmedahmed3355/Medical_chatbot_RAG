from unittest.mock import Mock, patch

import pytest

from app.common.custom_exception import CustomException
from app.components.retriever import (
    create_qa_chain,
    set_custom_prompt,
)


def test_set_custom_prompt():
    prompt = set_custom_prompt()

    assert "context" in prompt.input_variables
    assert "question" in prompt.input_variables


@patch(
    "app.components.retriever.RetrievalQA"
)
@patch(
    "app.components.retriever.load_llm"
)
@patch(
    "app.components.retriever.load_vector_store"
)
def test_create_qa_chain_success(
    mock_load_vector_store,
    mock_load_llm,
    mock_retrieval_qa,
):
    db = Mock()
    retriever = Mock()
    llm = Mock()
    chain = Mock()

    db.as_retriever.return_value = retriever
    mock_load_vector_store.return_value = db
    mock_load_llm.return_value = llm
    mock_retrieval_qa.from_chain_type.return_value = chain

    result = create_qa_chain()

    assert result is chain

    db.as_retriever.assert_called_once_with(
        search_kwargs={"k": 1}
    )

    mock_retrieval_qa.from_chain_type.assert_called_once()


@patch(
    "app.components.retriever.load_vector_store"
)
def test_create_qa_chain_missing_vector_store(
    mock_load_vector_store,
):
    mock_load_vector_store.return_value = None

    with pytest.raises(
        CustomException,
        match="Failed to create QA chain",
    ):
        create_qa_chain()


@patch(
    "app.components.retriever.load_llm"
)
@patch(
    "app.components.retriever.load_vector_store"
)
def test_create_qa_chain_missing_llm(
    mock_load_vector_store,
    mock_load_llm,
):
    mock_load_vector_store.return_value = Mock()
    mock_load_llm.return_value = None

    with pytest.raises(
        CustomException,
        match="Failed to create QA chain",
    ):
        create_qa_chain()
