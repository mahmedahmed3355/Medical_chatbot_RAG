from pathlib import Path
from typing import Sequence

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.components.embeddings import get_embedding_model
from app.config.config import DB_FAISS_PATH

logger = get_logger(__name__)


def load_vector_store(db_path: Path = DB_FAISS_PATH):
    try:
        if not db_path.exists():
            raise FileNotFoundError(f"Vector store does not exist: {db_path}")

        logger.info(
            "Loading vector store from %s",
            db_path,
        )

        embedding_model = get_embedding_model()

        return FAISS.load_local(
            str(db_path),
            embedding_model,
            allow_dangerous_deserialization=True,
        )

    except CustomException:
        raise

    except Exception as exc:
        logger.exception("Failed to load vector store")
        raise CustomException(
            "Failed to load vector store",
            exc,
        ) from exc


def save_vector_store(
    text_chunks: Sequence[Document],
    db_path: Path = DB_FAISS_PATH,
):
    try:
        if not text_chunks:
            raise ValueError("Cannot create a vector store from empty text chunks")

        logger.info(
            "Creating vector store from %s chunks",
            len(text_chunks),
        )

        embedding_model = get_embedding_model()

        db = FAISS.from_documents(
            list(text_chunks),
            embedding_model,
        )

        db_path.mkdir(
            parents=True,
            exist_ok=True,
        )

        db.save_local(str(db_path))

        logger.info(
            "Vector store successfully saved to %s",
            db_path,
        )

        return db

    except CustomException:
        raise

    except Exception as exc:
        logger.exception("Failed to save vector store")
        raise CustomException(
            "Failed to save vector store",
            exc,
        ) from exc
