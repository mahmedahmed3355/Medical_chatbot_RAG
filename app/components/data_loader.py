from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.components.pdf_loader import (
    create_text_chunks,
    load_pdf_files,
)
from app.components.vector_store import save_vector_store

logger = get_logger(__name__)


def process_and_store_pdfs():
    try:
        logger.info("Starting PDF ingestion pipeline")

        documents = load_pdf_files()

        text_chunks = create_text_chunks(
            documents,
        )

        vector_store = save_vector_store(
            text_chunks,
        )

        logger.info(
            "Vector store created successfully"
        )

        return vector_store

    except CustomException:
        raise

    except Exception as exc:
        logger.exception(
            "Failed to process and store PDFs"
        )
        raise CustomException(
            "Failed to process and store PDFs",
            exc,
        ) from exc


if __name__ == "__main__":
    process_and_store_pdfs()
