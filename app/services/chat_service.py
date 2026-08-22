from app.components.retriever import create_qa_chain


def answer_question(user_input: str) -> str:
    """Generate an answer for a user question using the QA chain."""
    qa_chain = create_qa_chain()

    response = qa_chain.invoke(
        {
            "query": user_input,
        }
    )

    return response.get(
        "result",
        "No response",
    )
