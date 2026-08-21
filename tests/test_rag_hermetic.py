import socket
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest


class NetworkAccessAttempted(RuntimeError):
    """Raised when a hermetic test attempts external network access."""


@pytest.fixture
def block_network(monkeypatch):
    def fail_network(*args, **kwargs):
        raise NetworkAccessAttempted(
            "External network access is forbidden in hermetic RAG tests."
        )

    monkeypatch.setattr(socket, "create_connection", fail_network)
    monkeypatch.setattr(socket, "getaddrinfo", fail_network)


def test_embedding_model_creation_is_hermetic(block_network):
    with patch(
        "app.components.embeddings.HuggingFaceEmbeddings"
    ) as embedding_cls:
        from app.components.embeddings import get_embedding_model

        result = get_embedding_model()

    assert result is embedding_cls.return_value
    embedding_cls.assert_called_once()


def test_llm_creation_is_hermetic_without_real_endpoint(
    block_network,
):
    with patch(
        "app.components.llm.HuggingFaceEndpoint"
    ) as endpoint_cls:
        from app.components.llm import load_llm

        result = load_llm(
            huggingface_repo_id="test/repository",
            hf_token="test-token",
        )

    assert result is endpoint_cls.return_value
    endpoint_cls.assert_called_once_with(
        repo_id="test/repository",
        huggingfacehub_api_token="test-token",
        temperature=0.3,
        max_new_tokens=256,
        return_full_text=False,
    )


def test_vector_store_save_is_hermetic(
    block_network,
    tmp_path,
):
    fake_embedding_model = MagicMock()
    fake_db = MagicMock()

    with patch(
        "app.components.vector_store.get_embedding_model",
        return_value=fake_embedding_model,
    ) as embedding_factory, patch(
        "app.components.vector_store.FAISS.from_documents",
        return_value=fake_db,
    ) as from_documents:
        from app.components.vector_store import save_vector_store

        documents = [MagicMock()]
        result = save_vector_store(
            documents,
            Path(tmp_path) / "vector_store",
        )

    assert result is fake_db
    embedding_factory.assert_called_once()
    from_documents.assert_called_once_with(
        documents,
        fake_embedding_model,
    )
    fake_db.save_local.assert_called_once()


def test_vector_store_load_is_hermetic(
    block_network,
    tmp_path,
):
    db_path = Path(tmp_path) / "vector_store"
    db_path.mkdir()

    fake_embedding_model = MagicMock()
    fake_db = MagicMock()

    with patch(
        "app.components.vector_store.get_embedding_model",
        return_value=fake_embedding_model,
    ) as embedding_factory, patch(
        "app.components.vector_store.FAISS.load_local",
        return_value=fake_db,
    ) as load_local:
        from app.components.vector_store import load_vector_store

        result = load_vector_store(db_path)

    assert result is fake_db
    embedding_factory.assert_called_once()
    load_local.assert_called_once_with(
        str(db_path),
        fake_embedding_model,
        allow_dangerous_deserialization=True,
    )


def test_retriever_pipeline_is_hermetic(block_network):
    fake_vector_store = MagicMock()
    fake_retriever = MagicMock()
    fake_vector_store.as_retriever.return_value = fake_retriever

    fake_llm = MagicMock()

    with patch(
        "app.components.retriever.load_vector_store",
        return_value=fake_vector_store,
    ) as load_vector_store_mock, patch(
        "app.components.retriever.load_llm",
        return_value=fake_llm,
    ) as load_llm_mock, patch(
        "app.components.retriever.RetrievalQA.from_chain_type"
    ) as chain_factory:
        from app.components.retriever import create_qa_chain

        result = create_qa_chain()

    assert result is chain_factory.return_value

    load_vector_store_mock.assert_called_once()
    load_llm_mock.assert_called_once()

    fake_vector_store.as_retriever.assert_called_once_with(
        search_kwargs={"k": 1},
    )

    chain_factory.assert_called_once()
