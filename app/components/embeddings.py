from langchain_huggingface import HuggingFaceEmbeddings

from app.common.custom_exception import CustomException
from app.common.logger import get_logger

logger = get_logger(__name__)

EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


def get_embedding_model():
    try:
        logger.info(
            "Initializing Hugging Face embedding model: %s",
            EMBEDDING_MODEL_NAME,
        )

        model = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL_NAME,
        )

        logger.info("Hugging Face embedding model loaded successfully")

        return model

    except CustomException:
        raise

    except Exception as exc:
        logger.exception("Failed to load embedding model")

        raise CustomException(
            "Failed to load embedding model",
            exc,
        ) from exc
