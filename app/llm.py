import os
import json
from urllib.request import Request, urlopen


OLLAMA_URL = os.getenv(
    "OLLAMA_URL",
    "http://host.docker.internal:11434/api/generate"
)
MODEL_NAME = "qwen2.5:3b"


def generate_answer(prompt: str) -> str:
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    request = Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=120) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result["response"]
 
def answer_question(question: str, top_k: int = 2) -> dict:
    from app.retriever import search_documents

    matches = search_documents(question, top_k)

    if not matches:
        return {
            "question": question,
            "answer": "I could not find relevant information in the documents.",
            "sources": [],
        }

    context = "\n\n".join(
        f"Source: {match['filename']}\n{match['content']}"
        for match in matches
    )

    prompt = f"""
You are a helpful DevOps document assistant.

Answer the user's question using the provided document context.
Explain the answer clearly in simple language.
If the context does not contain enough information, say so.
Do not invent facts or claim that information came from the documents
unless it is actually supported by the context.

Document context:
{context}

User question:
{question}

Answer:
"""

    answer = generate_answer(prompt)

    return {
        "question": question,
        "answer": answer,
        "sources": list(dict.fromkeys(
            match["filename"] for match in matches
        )),
    }
