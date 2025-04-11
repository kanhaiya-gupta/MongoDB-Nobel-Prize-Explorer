# MongoDB Nobel Prize Explorer ETL Pipeline

This project implements an **Extract, Transform, Load (ETL)** pipeline to process Nobel Prize data from a MongoDB database (`nobel.laureates`). It offers two execution modes:

1. **Serial Run**: Executes the pipeline locally using `main.py` for quick testing and development.
2. **Kubernetes Run**: Deploys a distributed pipeline using Kind, Argo Workflows, and Docker for scalability and orchestration.

The pipeline extracts laureate data, transforms it (e.g., standardizes dates, calculates ages), loads it into a `laureates_transformed` collection, and generates a visualization of laureates by country (`laureates_by_country.png`).

## Project Structure

```
MongoDB-Nobel-Prize-Explorer/
├── apply_manifests.sh          # Deploys Kubernetes manifests and runs Argo workflow
├── build_and_upload_images.sh  # Builds and loads Docker images into Kind
├── kind-config.yaml           # Kind cluster configuration
├── main.py                    # Entry point for serial ETL execution
├── .github/workflows/         # CI/CD workflows (if applicable)
├── datasets/
│   ├── laureates.json         # Input Nobel Prize laureates data
│   ├── prizes.json            # Input Nobel Prize data
├── Docker/
│   ├── Dockerfile.extract     # Image for extraction
│   ├── Dockerfile.transform   # Image for transformation
│   ├── Dockerfile.load        # Image for loading
│   ├── Dockerfile.visualize   # Image for visualization
├── docs/
│   ├── README.md              # This file
├── manifests/
│   ├── etl-workflow.yaml      # Argo Workflow definition
│   ├── mongodb.yaml           # MongoDB deployment and service
│   ├── pvc.yaml               # Persistent Volume Claim for data
├── notebooks/                 # Jupyter notebooks for exploration
├── notes/                     # Additional notes (e.g., PDFs)
├── results/
│   ├── laureates_by_country.png  # Output visualization
├── scripts/
│   ├── extract.py             # Extraction script
│   ├── load_chunk.py          # Loading script for chunks
│   ├── transform_chunk.py     # Transformation script for chunks
├── src/
│   ├── config.py              # Configuration settings
│   ├── database.py            # MongoDB connection logic
│   ├── load.py                # Data loading logic
│   ├── transform.py           # Data transformation logic
│   ├── visualization.py       # Visualization generation
│   ├── __init__.py
├── tests/                     # Unit tests for components
```

## Features

- **Extract**: Retrieves data from `nobel.laureates`.
- **Transform**: Processes data (e.g., date standardization, chunking).
- **Load**: Stores transformed data into `nobel.laureates_transformed`.
- **Visualize**: Creates a bar chart of laureates by country.
- **Flexible Execution**: Supports serial runs for simplicity and Kubernetes for distributed processing.

## Prerequisites

### For Serial Run
- **Python 3.11+**
- **MongoDB**: Local instance on `localhost:27017`
- **Dependencies**: `pymongo`, `matplotlib` (see `docs/requirements.txt`)

### For Kubernetes Run
- **Docker**
- **Kind**: Kubernetes in Docker
- **kubectl**
- **Argo CLI**: v3.5.8
- **MongoDB Tools**: `mongoimport`

Install tools:
```bash
# Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind && sudo mv ./kind /usr/local/bin/

# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl && sudo mv ./kubectl /usr/local/bin/

# Argo CLI
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.5.8/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64 && sudo mv argo-linux-amd64 /usr/local/bin/argo

# MongoDB Tools
sudo apt install mongodb-clients
```

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd MongoDB-Nobel-Prize-Explorer
   ```

2. **Install Python Dependencies** (Serial Run):
   ```bash
   pip install -r docs/requirements.txt
   ```

3. **Prepare MongoDB**:
   - Start MongoDB locally:
     ```bash
     mongod
     ```
   - Import data:
     ```bash
     mongoimport --uri mongodb://localhost:27017/nobel --collection laureates --file datasets/laureates.json
     ```

4. **Prepare Host Directories** (Kubernetes Run):
   ```bash
   mkdir -p /data/nobel-etl /data/mongo
   sudo chmod -R 777 /data
   ```

## Running the Pipeline

### Serial Run (Using `main.py`)
For quick testing or development:

1. Ensure MongoDB is running on `localhost:27017`.
2. Execute:
   ```bash
   python main.py
   ```
3. **Output**:
   - Transformed data in `nobel.laureates_transformed`.
   - Visualization: `results/laureates_by_country.png`.
   - Console logs of extraction, transformation, and loading steps.

### Kubernetes Run (Using Kind and Argo)

#### Step 1: Build and Load Docker Images
```bash
bash build_and_upload_images.sh
```
- Creates a Kind cluster (`nobel-etl-cluster`).
- Builds and loads images: `nobel-etl-extract`, `nobel-etl-transform`, `nobel-etl-load`, `nobel-etl-visualize`.

#### Step 2: Deploy and Run Workflow
```bash
bash apply_manifests.sh
```
- Deploys MongoDB, a PVC, and Argo Workflows.
- Submits `etl-workflow.yaml` and watches execution.

#### Step 3: Verify Outputs
- Data files:
  ```bash
  ls /data/nobel-etl
  ```
  - Expect `extracted_laureates.json`, `transformed_chunk_*.json`.
- Visualization:
  ```bash
  ls results/
  ```
  - Expect `laureates_by_country.png`.

#### Workflow Details
- **Extract**: Writes laureates to `/data/extracted_laureates.json`.
- **Transform**: Splits into chunks (e.g., 4 chunks), writes to `/data/transformed_chunk_*.json`.
- **Load**: Loads chunks into MongoDB.
- **Visualize**: Generates a plot from transformed data.

## Configuration

- **Serial Run**: Edit `src/config.py`:
  - `MONGODB_URI`: Default `mongodb://localhost:27017/`.
  - `DATABASE_NAME`: Default `nobel`.
- **Kubernetes Run**: Modify environment variables in `etl-workflow.yaml` or Dockerfiles:
  - `MONGODB_URI`: `mongodb://mongodb-service:27017/`.
  - `CHUNK_SIZE`: Adjust in `transform-task`.

## Troubleshooting

### Serial Run
- **MongoDB Connection**:
  ```bash
  mongo --host localhost --port 27017
  ```
- **Missing Output**:
  - Check `nobel.laureates` has data.

### Kubernetes Run
- **Pod Logs**:
  ```bash
  kubectl logs <pod-name> -n default --context kind-nobel-etl-cluster
  ```
- **Workflow Status**:
  ```bash
  argo list -n default --context kind-nobel-etl-cluster
  argo logs -n default @latest --context kind-nobel-etl-cluster
  ```
- **RBAC Issues**:
  - Apply `manifests/argo-rbac.yaml` if permissions errors occur (see previous responses).

## Cleanup

### Serial Run
- Remove output files:
  ```bash
  rm results/laureates_by_country.png
  ```

### Kubernetes Run
- Delete cluster and images:
  ```bash
  kind delete cluster --name nobel-etl-cluster
  docker rm -f kind-registry
  docker rmi -f $(docker images -q localhost:5000/nobel-etl-*)
  ```

## Sample Data

Expected `laureates.json` structure:
```json
{
  "id": "2",
  "firstname": "Hendrik Antoon",
  "surname": "Lorentz",
  "born": "1853-07-18",
  "bornCountry": "the Netherlands",
  "prizes": [{"year": "1902", "category": "physics"}]
}
```

## Contributing

Submit issues or pull requests to enhance functionality, add tests, or improve docs.

## License

MIT License (see `LICENSE` file if present).

---

### Notes
- **Serial Run**: Assumes `main.py` orchestrates `extract.py`, `transform.py`, `load.py`, and `visualization.py`. If your `main.py` differs, I can refine this section with its actual logic.
- **Kubernetes Run**: Reflects your current setup with Argo Workflows and chunked processing. The RBAC fix is referenced but not repeated unless needed.
- **Placement**: Save as `docs/README.md` per your structure.
- **Customization**: Replace `<repository-url>` with your repo link if applicable.

Let me know if you want to tweak any part (e.g., add specific script details or test instructions)!
