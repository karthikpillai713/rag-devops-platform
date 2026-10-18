
from fastapi import FastAPI
from pydantic import BaseModel

from app.llm import answer_question

app = FastAPI(
    title="RAG DevOps Platform",
    description="A locally hosted AI document assistant",
    version="1.0.0",
)


class SearchRequest(BaseModel):
    question: str
    top_k: int = 2


@app.get("/")
def home():
    return {
        "message": "RAG DevOps Platform is running!",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/search")
def search(request: SearchRequest):
    return answer_question(
        question=request.question,
        top_k=request.top_k,
    )
