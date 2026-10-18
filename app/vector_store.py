
import chromadb

from app.chunker import split_text
from app.document_loader import load_documents


DB_DIR = "data/chroma_db"
COLLECTION_NAME = "devops_documents"


def build_vector_store():
    client = chromadb.PersistentClient(path=DB_DIR)

    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )

    documents = load_documents()

    for document in documents:
        chunks = split_text(document["content"])

        for index, chunk in enumerate(chunks):
            collection.upsert(
                ids=[f"{document['filename']}-{index}"],
                documents=[chunk],
                metadatas=[{
                    "filename": document["filename"],
                    "chunk_index": index,
                }],
            )

    return collection
