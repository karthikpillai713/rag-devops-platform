
from app.vector_store import build_vector_store


def search_documents(question: str, top_k: int = 2):
    collection = build_vector_store()

    results = collection.query(
        query_texts=[question],
        n_results=min(top_k, collection.count()),
    )

    matches = []

    if results["documents"] and results["documents"][0]:
        for document, metadata, distance in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            matches.append({
                "content": document,
                "filename": metadata["filename"],
                "distance": distance,
            })

    return matches
