from pathlib import Path

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


class DeterministicMedicalEmbeddings(Embeddings):
    """Deterministic offline embeddings for RAG integration tests."""

    def __init__(self) -> None:
        self.vectors = {
            "diabetes": [1.0, 0.0, 0.0],
            "hypertension": [0.0, 1.0, 0.0],
            "vaccination": [0.0, 0.0, 1.0],
            "high blood pressure": [0.0, 1.0, 0.0],
        }

    def _embed(self, text: str) -> list[float]:
        normalized = text.lower()

        for keyword, vector in self.vectors.items():
            if keyword in normalized:
                return vector

        return [0.0, 0.0, 0.0]

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        return [self._embed(text) for text in texts]

    def embed_query(self, text: str) -> list[float]:
        return self._embed(text)


def test_offline_rag_pipeline_chunk_embed_save_load_and_retrieve(
    tmp_path: Path,
) -> None:
    """
    End-to-end offline integration test for the core RAG retrieval pipeline.

    Covers:
    documents -> embeddings -> FAISS -> save -> load -> similarity retrieval
    """

    documents = [
        Document(
            page_content=(
                "Diabetes is a chronic condition that affects how the body processes blood glucose."
            ),
            metadata={"source": "medical_a", "topic": "diabetes"},
        ),
        Document(
            page_content=(
                "Hypertension is a condition in which blood pressure remains consistently elevated."
            ),
            metadata={"source": "medical_b", "topic": "hypertension"},
        ),
        Document(
            page_content=(
                "Vaccination helps the immune system recognize and respond "
                "to specific infectious agents."
            ),
            metadata={"source": "medical_c", "topic": "vaccination"},
        ),
    ]

    embeddings = DeterministicMedicalEmbeddings()

    vector_store = FAISS.from_documents(
        documents,
        embeddings,
    )

    save_path = tmp_path / "faiss_index"

    vector_store.save_local(str(save_path))

    assert save_path.exists()
    assert (save_path / "index.faiss").exists()
    assert (save_path / "index.pkl").exists()

    loaded_vector_store = FAISS.load_local(
        str(save_path),
        embeddings,
        allow_dangerous_deserialization=True,
    )

    results = loaded_vector_store.similarity_search(
        "What condition is related to high blood pressure?",
        k=2,
    )

    assert len(results) == 2

    retrieved_topics = {document.metadata["topic"] for document in results}

    assert "hypertension" in retrieved_topics
