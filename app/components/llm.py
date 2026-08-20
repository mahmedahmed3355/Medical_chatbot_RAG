from typing import Optional

from langchain_huggingface import HuggingFaceEndpoint

from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.config.config import HF_TOKEN, HUGGINGFACE_REPO_ID

logger = get_logger(__name__)


def load_llm(
    huggingface_repo_id: str = HUGGINGFACE_REPO_ID,
    hf_token: Optional[str] = HF_TOKEN,
):
    try:
        if not huggingface_repo_id:
            raise ValueError("A Hugging Face repository ID is required")

        if not hf_token:
            raise ValueError(
                "HF_TOKEN is required to initialize the Hugging Face endpoint"
            )

        logger.info(
            "Loading Hugging Face LLM: %s",
            huggingface_repo_id,
        )

        llm = HuggingFaceEndpoint(
            repo_id=huggingface_repo_id,
            huggingfacehub_api_token=hf_token,
            temperature=0.3,
            max_new_tokens=256,
            return_full_text=False,
        )

        logger.info("Hugging Face LLM loaded successfully")

        return llm

    except CustomException:
        raise

    except Exception as exc:
        logger.exception("Failed to load LLM")
        raise CustomException(
            "Failed to load LLM",
            exc,
        ) from exc
