
from pathlib import Path

DOCUMENTS_DIR = Path(__file__).resolve().parent.parent / "documents"


def load_documents():
    documents = []

    for file_path in DOCUMENTS_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        documents.append({
            "filename": file_path.name,
            "content": content,
        })

    return documents
