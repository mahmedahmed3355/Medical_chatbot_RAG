from pathlib import Path
from typing import Sequence

from langchain_community.document_loaders import DirectoryLoader, PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.config.config import CHUNK_OVERLAP, CHUNK_SIZE, DATA_PATH

logger = get_logger(__name__)


def load_pdf_files(data_path: Path = DATA_PATH):
    try:
        if not data_path.exists():
            raise FileNotFoundError(f"Data path does not exist: {data_path}")

        logger.info("Loading PDF files from %s", data_path)

        loader = DirectoryLoader(
            str(data_path),
            glob="*.pdf",
            loader_cls=PyPDFLoader,
        )

        documents = loader.load()

        if not documents:
            raise ValueError(f"No PDF documents found in: {data_path}")

        logger.info("Successfully loaded %s document pages", len(documents))
        return documents

    except CustomException:
        raise

    except Exception as exc:
        logger.exception("Failed to load PDF files")
        raise CustomException(
            "Failed to load PDF files",
            exc,
        ) from exc


def create_text_chunks(documents: Sequence):
    try:
        if not documents:
            raise ValueError("Cannot create chunks from an empty document collection")

        logger.info(
            "Splitting %s documents into chunks",
            len(documents),
        )

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP,
        )

        text_chunks = text_splitter.split_documents(documents)

        if not text_chunks:
            raise ValueError("Text splitting produced no chunks")

        logger.info(
            "Successfully generated %s text chunks",
            len(text_chunks),
        )

        return text_chunks

    except CustomException:
        raise

    except Exception as exc:
        logger.exception("Failed to create text chunks")
        raise CustomException(
            "Failed to create text chunks",
            exc,
        ) from exc
