import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

HF_TOKEN = os.getenv("HF_TOKEN")

HUGGINGFACE_REPO_ID = os.getenv(
    "HUGGINGFACE_REPO_ID",
    "mistralai/Mistral-7B-Instruct-v0.3",
)

DB_FAISS_PATH = Path(
    os.getenv(
        "DB_FAISS_PATH",
        PROJECT_ROOT / "vectorstore" / "db_faiss",
    )
)

DATA_PATH = Path(
    os.getenv(
        "DATA_PATH",
        PROJECT_ROOT / "data",
    )
)

CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))

if CHUNK_SIZE <= 0:
    raise ValueError("CHUNK_SIZE must be greater than zero")

if CHUNK_OVERLAP < 0:
    raise ValueError("CHUNK_OVERLAP cannot be negative")

if CHUNK_OVERLAP >= CHUNK_SIZE:
    raise ValueError("CHUNK_OVERLAP must be smaller than CHUNK_SIZE")
