from pathlib import Path

from setuptools import find_packages, setup

requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()

setup(
    name="medical-rag-chatbot",
    version="0.1.0",
    description="Medical RAG chatbot built with LangChain, FAISS, and Flask",
    packages=find_packages(),
    install_requires=[
        requirement.strip()
        for requirement in requirements
        if requirement.strip() and not requirement.strip().startswith("#")
    ],
    python_requires=">=3.12",
)
