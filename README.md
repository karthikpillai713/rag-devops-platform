# RAG DevOps Platform

A locally hosted Retrieval-Augmented Generation (RAG) application that answers questions using DevOps documentation. It combines document retrieval with a local Large Language Model (LLM), packaged using Docker and tested automatically through GitHub Actions.

## Features

- **Document retrieval:** Retrieves relevant information from DevOps documentation using ChromaDB.
- **Local AI responses:** Uses Ollama with the Qwen2.5 3B model to generate answers based on retrieved context.
- **REST API:** Built with FastAPI.
- **Containerization:** Packages the application using Docker.
- **Persistent storage:** Uses a Docker volume to preserve the ChromaDB database.
- **Automated testing:** Uses pytest and GitHub Actions for continuous integration.

## Tech Stack

- Python
- FastAPI
- ChromaDB
- Ollama
- Qwen2.5 3B
- Docker
- Docker Compose
- GitHub Actions
- pytest

## Architecture

1. A user submits a question through the REST API.
2. The application searches the ChromaDB vector database for relevant document chunks.
3. The retrieved context and question are passed to the local Ollama model.
4. The model generates an answer based on the provided context.
5. The API returns the answer along with its source documents.

## Project Structure

```text
rag-devops-platform/
├── .github/
│   └── workflows/
│       └── ci.yml
├── app/
│   ├── main.py
│   ├── llm.py
│   ├── retriever.py
│   └── vector_store.py
├── data/
├── documents/
│   └── devops-basics.txt
├── tests/
│   └── test_api.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Prerequisites

- Docker Desktop with Docker Compose
- Ollama installed and running on the host machine
- Git

## Run Locally with Docker Compose

### 1. Download the model

Install and start Ollama, then run:

```bash
ollama pull qwen2.5:3b
```

### 2. Start the application

Clone the repository and enter the project directory:

```bash
git clone https://github.com/karthikpillai713/rag-devops-platform.git
cd rag-devops-platform
```

Start the application:

```bash
docker compose up --build -d
```

The API will be available at:

- API: http://localhost:8000
- Interactive API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/health

### 3. Test the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### 4. Ask a question

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Docker used for?"}'
```

The API returns the question, generated answer, and source filenames.

### 5. Stop the application

```bash
docker compose down
```

The named Docker volume preserves the application's stored data when the container is removed. Do not remove the volume if you want to keep that data.

## Testing

Run the automated tests locally from the project directory:

```bash
python -m pytest -v
```

The current test suite covers the home, health, and search endpoints.

## Continuous Integration

GitHub Actions runs automatically when code is pushed to the `main` branch or a pull request targets `main`.

The workflow:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs the dependencies.
4. Runs the pytest test suite.

Workflow configuration: `.github/workflows/ci.yml`

## Future Improvements

- Add more DevOps documentation sources.
- Improve error handling and input validation.
- Add retrieval-quality and response-quality tests.
- Add automated Docker image publishing.
- Improve monitoring and logging.

## Author

**Karthik S Pillai**

GitHub: https://github.com/karthikpillai713
