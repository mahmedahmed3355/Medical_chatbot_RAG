from langchain_classic.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

from app.common.custom_exception import CustomException
from app.common.logger import get_logger
from app.components.llm import load_llm
from app.components.vector_store import load_vector_store
from app.config.config import HF_TOKEN, HUGGINGFACE_REPO_ID

logger = get_logger(__name__)

CUSTOM_PROMPT_TEMPLATE = """
Answer the following medical question in 2-3 lines maximum
using only the information provided in the context.

Context:
{context}

Question:
{question}

Answer:
"""


def set_custom_prompt():
    return PromptTemplate(
        template=CUSTOM_PROMPT_TEMPLATE,
        input_variables=["context", "question"],
    )


def create_qa_chain():
    try:
        logger.info("Loading vector store for retrieval")

        db = load_vector_store()

        if db is None:
            raise ValueError("Vector store could not be loaded")

        llm = load_llm(
            huggingface_repo_id=HUGGINGFACE_REPO_ID,
            hf_token=HF_TOKEN,
        )

        if llm is None:
            raise ValueError("LLM could not be loaded")

        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=db.as_retriever(
                search_kwargs={"k": 1},
            ),
            return_source_documents=False,
            chain_type_kwargs={
                "prompt": set_custom_prompt(),
            },
        )

        logger.info("QA chain created successfully")

        return qa_chain

    except CustomException:
        raise

    except Exception as exc:
        logger.exception("Failed to create QA chain")
        raise CustomException(
            "Failed to create QA chain",
            exc,
        ) from exc
