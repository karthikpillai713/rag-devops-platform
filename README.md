# RAG DevOps Platform

A locally hosted Retrieval-Augmented Generation (RAG) application that answers questions using DevOps documentation. This project combines document retrieval, a local Large Language Model (LLM), containerization, Kubernetes orchestration, automated CI/CD, and Prometheus/Grafana monitoring.

## Features

- **Retrieval-Augmented Generation:** Retrieves relevant document chunks using ChromaDB and generates context-based answers.
- **Local AI inference:** Uses Ollama with the Qwen2.5 3B model.
- **REST API:** Exposes application endpoints through FastAPI.
- **Containerization:** Packages the application using Docker.
- **Persistent storage:** Uses persistent storage for ChromaDB data in the Kubernetes deployment.
- **Kubernetes orchestration:** Deploys and manages the application on Minikube.
- **Automated testing:** Runs pytest tests through GitHub Actions.
- **Docker image publishing:** Builds and pushes Docker images to Docker Hub.
- **Automated deployment:** Uses a self-hosted GitHub Actions runner to deploy successful builds to the local Kubernetes cluster.
- **Monitoring and observability:** Exposes application metrics for Prometheus and visualizes them using Grafana.

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| API framework | FastAPI |
| Vector database | ChromaDB |
| LLM inference | Ollama, Qwen2.5 3B |
| Containerization | Docker, Docker Compose |
| Orchestration | Kubernetes, Minikube |
| CI/CD | GitHub Actions, self-hosted runner |
| Container registry | Docker Hub |
| Monitoring | Prometheus, Grafana |
| Metrics instrumentation | prometheus-fastapi-instrumentator |
| Testing | pytest |

## Architecture

### RAG application flow

1. A user submits a question through the REST API.
2. The application retrieves relevant document chunks from ChromaDB.
3. The retrieved context and question are passed to the configured local Ollama model.
4. The model generates an answer using the retrieved context.
5. The API returns the answer and source filenames.

### DevOps and deployment flow

1. A code change is pushed to the `main` branch.
2. GitHub Actions checks out the repository, installs dependencies, and runs automated tests.
3. The workflow builds a Docker image and pushes it to Docker Hub using `latest` and commit-specific tags.
4. After the test-and-build job succeeds, the self-hosted runner executes the deployment job.
5. The deployment job updates the `rag-app` Kubernetes deployment to the image built for that commit.
6. Kubernetes performs a rollout, and the workflow waits for rollout completion.

The self-hosted runner operates in the local WSL environment and requires GitHub connectivity, a running Minikube cluster, and valid Kubernetes access.

### Monitoring flow

1. FastAPI exposes application metrics at `/metrics`.
2. Prometheus scrapes the application metrics through a Kubernetes ServiceMonitor.
3. Grafana visualizes application health, request rate, latency, and HTTP error rate.

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
├── k8s/
│   ├── deployment.yaml
│   ├── restore-pod.yaml
│   ├── service.yaml
│   └── storage.yaml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

*The tree above summarizes the main files; adjust it if your current repository structure differs.*

## Prerequisites

- Git
- Python 3.12
- Docker Desktop with Docker Compose
- Ollama and the required model for local execution
- Minikube and kubectl for Kubernetes deployment
- A GitHub repository and Docker Hub repository for CI/CD
- A configured self-hosted GitHub Actions runner for deployment to the local cluster

## Run Locally with Docker Compose

### 1. Download the model

Install and start Ollama, then run:

```bash
ollama pull qwen2.5:3b
```

Ensure the application container can reach the Ollama service using the address configured for your environment.

### 2. Clone the repository

```bash
git clone https://github.com/karthikpillai713/rag-devops-platform.git
cd rag-devops-platform
```

### 3. Start the application

```bash
docker compose up --build -d
```

The API is expected at:

- API: `http://localhost:8000`
- Interactive documentation: `http://localhost:8000/docs`
- Health endpoint: `http://localhost:8000/health`

These addresses assume the ports configured in your Docker Compose file.

### 4. Test the health endpoint

```bash
curl http://localhost:8000/health
```

Expected response, if configured as shown:

```json
{"status":"ok"}
```

### 5. Ask a question

```bash
curl -X POST http://localhost:8000/search \
  -H "Content-Type: application/json" \
  -d '{"question":"What is Docker used for?"}'
```

The API returns the question, generated answer, and source filenames.

### 6. Stop the application

```bash
docker compose down
```

Keep the named data volume if you want to preserve its contents. Do not remove volumes unless you intentionally want to delete their data.

## Kubernetes Deployment

The application is deployed to a local Minikube cluster using Kubernetes manifests and a persistent volume claim.

Check the cluster:

```bash
kubectl get nodes
```

Inspect the application deployment and pods:

```bash
kubectl get deployment,pods,services
```

Check persistent storage:

```bash
kubectl get pvc
```

Check rollout status:

```bash
kubectl rollout status deployment/rag-app
```

To access the API locally through a port-forward:

```bash
kubectl port-forward deployment/rag-app 8001:8000
```

Then open `http://localhost:8001/docs`.

Keep the port-forward process running while using this access method. The cluster and application must also be running.

## Monitoring with Prometheus and Grafana

The application exposes metrics at:

```text
/metrics
```

Prometheus scrapes the application through its configured ServiceMonitor. Grafana uses Prometheus as a data source to visualize application metrics.

The monitoring dashboard includes:

- Application health
- Request rate
- P95 response latency
- HTTP error rate

To inspect the Prometheus target, open the Prometheus Targets page and confirm the `rag-app` target is `UP`.

Grafana and Prometheus are exposed locally through Kubernetes port-forwards in this development environment. Their availability depends on the monitoring pods and port-forward processes running.

## Testing

Run the automated tests from the repository root:

```bash
python -m pytest -v
```

The test suite covers the application's API endpoints. The GitHub Actions workflow runs the tests on pushes to `main` and pull requests targeting `main`.

## Continuous Integration and Deployment

Workflow configuration: `.github/workflows/ci.yml`

### CI: Test, build, and publish

On pushes to `main`, the workflow:

1. Checks out the repository.
2. Sets up Python 3.12.
3. Installs dependencies.
4. Runs pytest.
5. Authenticates with Docker Hub using GitHub Actions secrets.
6. Builds and publishes Docker images tagged `latest` and with the commit SHA.

Pull requests run the test-and-build job's test steps without publishing an image.

### CD: Deploy to Minikube

After the test-and-build job succeeds on a push to `main`, the deployment job:

1. Runs on the self-hosted runner.
2. Verifies Kubernetes access.
3. Updates the `rag-app` deployment to the commit-specific image.
4. Waits for the Kubernetes rollout to complete.

**Important:** This deployment targets a local Minikube cluster. The self-hosted runner must be online and Minikube must be running for automated deployments to succeed. Do not expose the Kubernetes API publicly just to enable this workflow.

Configure the following GitHub Actions secrets for image publishing:

- `DOCKERHUB_USERNAME`
- `DOCKERHUB_TOKEN`

## Validation Results

The following checks have been completed in the development environment:

- GitHub Actions test-and-build job succeeded.
- Docker image publishing completed through the workflow.
- Automated deployment job succeeded.
- Kubernetes rollout completed successfully.
- The application pod reached `Running` with readiness `1/1`.
- The existing `rag-data` PVC remained `Bound`.
- The Swagger UI returned a successful RAG response with source attribution.
- Prometheus reported the application target as `UP`.
- Grafana dashboard panels continued displaying metrics after deployment.

## Future Improvements

- Expand the document collection and retrieval-quality tests.
- Add response-quality and failure-path tests.
- Add alerting rules for elevated error rates and latency.
- Improve structured logging and troubleshooting documentation.
- Add automated rollback procedures and deployment notifications.
- Document runner setup and recovery after a WSL or Minikube restart.

## Author

**Karthik S Pillai**

GitHub: https://github.com/karthikpillai713
