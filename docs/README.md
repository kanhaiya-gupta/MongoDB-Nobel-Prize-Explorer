# Nobel Laureates ETL Pipeline

This project builds an **Extract, Transform, Load (ETL)** pipeline to process Nobel Prize data from the MongoDB "nobel" database, which includes "laureates" and "prizes" collections. It extracts data using the connected client (client.nobel), transforms it by standardizing dates and calculating ages at award time, and loads the results into a new "laureates_transformed" collection. Leveraging MongoDB’s NoSQL flexibility, the pipeline handles dynamic schemas to streamline data processing. The final step generates a visualization of laureates by country based on the transformed data. All code and outputs are crafted to align with the project’s analytical goals.

## Project Structure

```
nobel_etl/
├── src/                  # Core Python modules
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Configuration settings
│   ├── database.py       # MongoDB connection and extraction
│   ├── transform.py      # Data transformation logic
│   ├── load.py           # Data loading into MongoDB
│   └── visualization.py  # Visualization generation
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_transform.py
│   ├── test_load.py
│   └── test_visualization.py
├── data/                 # Data storage
│   └── README.md         # Instructions for data files
├── docs/                 # Documentation
│   ├── README.md         # Additional project docs
│   └── requirements.txt  # Dependencies
├── main.py               # Entry point for the ETL pipeline
├── README.md             # This file
└── LICENSE               # MIT License
```

## Features
- **Extract**: Retrieves laureate data from the `nobel.laureates` collection in MongoDB.
- **Transform**: Standardizes dates, calculates age at award time, and enriches prize data.
- **Load**: Stores transformed data into `nobel.laureates_transformed`.
- **Visualization**: Generates a bar chart of the top 10 countries by laureate count, saved as `laureates_by_country.png`.
- **Comparison**: Compares the number of laureates vs. prizes to determine a true statement.
- **Modular Design**: Separates concerns into distinct modules with a configurable setup.
- **Testing**: Includes unit tests for each component.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **MongoDB**: A local MongoDB instance running on `localhost:27017` (default port).
- **Dependencies**: Listed in `docs/requirements.txt`.

## Setup Instructions

### 1. Install MongoDB
- Download and install MongoDB Community Server from [MongoDB Download Center](https://www.mongodb.com/try/download/community).
- Start MongoDB:
  - On Windows (if installed as a service): It should start automatically; check `services.msc`.
  - Manually: Run `mongod` from the MongoDB `bin` directory (e.g., `C:\Program Files\MongoDB\Server\8.0\bin`).

### 2. Clone the Repository
```bash
git clone <repository-url>
cd nobel_etl
```

### 3. Install Dependencies
```bash
pip install -r docs/requirements.txt
```
This installs `pymongo` for MongoDB interaction and `matplotlib` for visualization.

### 4. Prepare Data
- Ensure your Nobel Prize data is loaded into the `nobel` database:
  - If you have a `laureates.json` file, place it in the `data/` directory and load it into MongoDB manually (see below) or extend `database.py` to handle this.
  - Example manual load:
    ```python
    from pymongo import MongoClient
    import json
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nobel']
    with open('data/laureates.json', 'r') as f:
        data = json.load(f)
        db.laureates.insert_many(data)
    client.close()
    ```

## Usage

### Running the ETL Pipeline
1. Ensure MongoDB is running.
2. Execute the main script:
   ```bash
   python main.py
   ```
3. Expected Output:
   - Connection confirmation.
   - Number of extracted, transformed, and loaded laureates.
   - Comparison of laureates vs. prizes.
   - A file `laureates_by_country.png` in the root directory.

### Running Tests
```bash
python -m unittest discover tests
```
This runs all unit tests to verify functionality. Note: Tests assume a running MongoDB instance with data in `nobel.laureates`.

## Configuration
Edit `src/config.py` to customize:
- `MONGODB_URI`: Change if your MongoDB instance is not on `localhost:27017`.
- `DATABASE_NAME`: Set to a different database if needed.
- `TARGET_COLLECTION`: Rename the output collection.
- `VISUALIZATION_OUTPUT`: Change the visualization file name/path.

## Sample Data
The pipeline expects data in the `nobel.laureates` collection with a structure like:
```json
{
  "id": "2",
  "firstname": "Hendrik Antoon",
  "surname": "Lorentz",
  "born": "1853-07-18",
  "died": "1928-02-04",
  "bornCountry": "the Netherlands",
  "gender": "male",
  "prizes": [
    {
      "year": "1902",
      "category": "physics",
      "share": "2",
      "motivation": "..."
    }
  ]
}
```

## Extending the Pipeline
- **Add Data Loading**: Modify `database.py` to load `laureates.json` from `data/`.
- **More Visualizations**: Update `visualization.py` for additional charts (e.g., prizes by category).
- **Error Handling**: Add try-except blocks for robustness.
- **CLI Options**: Use `argparse` in `main.py` for runtime configuration.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Feel free to submit issues or pull requests to enhance the pipeline. See `docs/README.md` for more details.

## Contact
For questions, reach out to [Your Name/Email] or open an issue on the repository.
```

---

### Notes
- **Placement**: Save this as `README.md` in the root directory (`nobel_etl/`).
- **Customization**: Replace `<repository-url>` and `[Your Name/Email]` with your actual details if hosting this on GitHub or similar.
- **Data Loading**: I included a manual loading example since your `laureates.json` isn’t automatically loaded yet. If you want this integrated, I can update `database.py` and `main.py`.
- **Tests**: The README notes that tests require MongoDB and data—consider mocking for CI environments if needed.

This README should give anyone a clear path to set up and run your project. Let me know if you’d like to adjust anything!


Below is a concise and informative `README.md` tailored for your "MongoDB-Nobel-Prize-Explorer" project, which implements an ETL (Extract, Transform, Load) pipeline using Kubernetes with Kind, Argo Workflows, and MongoDB. This README assumes your project structure and goals based on the provided context, focusing on processing Nobel Prize data (`laureates.json`) and generating visualizations.

---

# MongoDB Nobel Prize Explorer ETL Pipeline

This project implements an **Extract, Transform, Load (ETL)** pipeline to process Nobel Prize data using **Kubernetes**, orchestrated with **Kind** (Kubernetes IN Docker) and **Argo Workflows**. It extracts data from a MongoDB database, transforms it into structured JSON chunks, loads the processed data back into MongoDB, and generates visualizations (e.g., laureates by country).

## Project Structure

```
MongoDB-Nobel-Prize-Explorer/
├── build_and_upload_images.sh  # Builds and loads Docker images into Kind
├── apply_manifests.sh          # Deploys manifests and submits the Argo workflow
├── kind-config.yaml           # Kind cluster configuration
├── main.py                    # (Optional) Main script for manual execution
├── Docker/
│   ├── Dockerfile.extract     # Docker image for extraction
│   ├── Dockerfile.transform   # Docker image for transformation
│   ├── Dockerfile.load        # Docker image for loading
│   ├── Dockerfile.visualize   # Docker image for visualization
├── manifests/
│   ├── pvc.yaml               # Persistent Volume Claim for data storage
│   ├── mongodb.yaml           # MongoDB deployment and service
│   ├── etl-workflow.yaml      # Argo Workflow definition
├── src/
│   ├── config.py              # Configuration settings (e.g., MongoDB URI)
│   ├── database.py            # MongoDB connection and query logic
│   ├── load.py                # Data loading logic
│   ├── transform.py           # Data transformation logic
│   ├── visualization.py       # Visualization generation (e.g., matplotlib)
│   ├── __init__.py
├── scripts/
│   ├── extract.py             # Extraction script
│   ├── transform_chunk.py     # Transformation script for chunks
│   ├── load_chunk.py          # Loading script for chunks
├── datasets/
│   ├── laureates.json         # Input Nobel Prize laureates data
│   ├── prizes.json            # Input Nobel Prize data
├── results/
│   ├── laureates_by_country.png  # Output visualization
├── docs/
│   ├── README.md              # This file
├── notebooks/                 # Jupyter notebooks for exploration
├── notes/                     # Additional notes (e.g., PDFs)
├── tests/                     # Unit tests
```

## Prerequisites

- **Docker**: For building and running container images.
- **Kind**: For running a local Kubernetes cluster.
- **kubectl**: For interacting with Kubernetes.
- **Argo CLI**: For managing Argo Workflows.
- **MongoDB Tools**: `mongoimport` for importing data.
- **Python 3.11**: For local development and testing.
- **WSL2** (optional): If running on Windows.

Install dependencies:
```bash
# Install Kind
curl -Lo ./kind https://kind.sigs.k8s.io/dl/v0.23.0/kind-linux-amd64
chmod +x ./kind
sudo mv ./kind /usr/local/bin/

# Install kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x ./kubectl
sudo mv ./kubectl /usr/local/bin/

# Install Argo CLI
curl -sLO https://github.com/argoproj/argo-workflows/releases/download/v3.5.8/argo-linux-amd64.gz
gunzip argo-linux-amd64.gz
chmod +x argo-linux-amd64
sudo mv argo-linux-amd64 /usr/local/bin/argo

# Install dos2unix (for WSL2)
sudo apt-get install -y dos2unix
```

## Setup

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd MongoDB-Nobel-Prize-Explorer
   ```

2. **Prepare Host Directories**:
   - Create directories for persistent data:
     ```bash
     mkdir -p /data/nobel-etl /data/mongo
     sudo chmod -R 777 /data
     ```

3. **Import Initial Data** (optional):
   - If starting with raw data:
     ```bash
     kubectl apply -f manifests/mongodb.yaml
     kubectl port-forward svc/mongodb-service 27017:27017 -n default &
     mongoimport --uri mongodb://localhost:27017/nobel --collection laureates --file datasets/laureates.json
     ```

## Running the ETL Pipeline

### Step 1: Build and Load Docker Images
Build the Docker images and load them into the Kind cluster:
```bash
bash build_and_upload_images.sh
```

- **What it does**:
  - Creates a Kind cluster (`nobel-etl-cluster`) if not present.
  - Starts a local Docker registry (`localhost:5000`).
  - Builds images: `nobel-etl-extract`, `nobel-etl-transform`, `nobel-etl-load`, `nobel-etl-visualize`.
  - Pushes images to the local registry and loads them into the cluster.

- **Verify**:
  ```bash
  docker images | grep nobel-etl
  kind get clusters
  ```

### Step 2: Deploy Manifests and Run Workflow
Deploy Kubernetes resources and execute the ETL workflow:
```bash
bash apply_manifests.sh
```

- **What it does**:
  - Switches to the `kind-nobel-etl-cluster` context.
  - Installs Argo Workflows in the `argo` namespace.
  - Applies `pvc.yaml` for persistent storage.
  - Deploys MongoDB via `mongodb.yaml`.
  - Submits the `etl-workflow.yaml` Argo Workflow and watches it to completion.

- **Verify**:
  - Check cluster nodes:
    ```bash
    kubectl get nodes --context kind-nobel-etl-cluster
    ```
  - Check Argo resources:
    ```bash
    kubectl get all -n argo --context kind-nobel-etl-cluster
    ```
  - Monitor workflow:
    ```bash
    argo list -n default --context kind-nobel-etl-cluster
    argo logs -n default @latest --context kind-nobel-etl-cluster
    ```

### Step 3: Check Outputs
- **Transformed Data**:
  ```bash
  ls /data/nobel-etl
  ```
  - Expect files like `extracted_laureates.json`, `transformed_chunk_0.json`.

- **Visualization**:
  ```bash
  ls results/
  ```
  - Expect `laureates_by_country.png`.

## Pipeline Overview

1. **Extract** (`nobel-etl-extract`):
   - Connects to MongoDB, extracts laureates data, and writes to `/data/extracted_laureates.json`.

2. **Transform** (`nobel-etl-transform`):
   - Reads `extracted_laureates.json`, processes it into chunks, and writes to `/data/transformed_chunk.json`.

3. **Load** (`nobel-etl-load`):
   - Loads `transformed_chunk.json` back into MongoDB.

4. **Visualize** (`nobel-etl-visualize`):
   - Queries MongoDB and generates a visualization (e.g., laureates by country) saved to `results/`.

## Customization

- **MongoDB URI**: Edit `src/config.py` or set `MONGODB_URI` environment variables in Dockerfiles.
- **Chunk Size**: Adjust `CHUNK_SIZE` in `Dockerfile.transform`.
- **Workflow**: Modify `manifests/etl-workflow.yaml` to change steps or parallelism.

## Troubleshooting

- **Image Build Fails**:
  ```bash
  docker build -t localhost:5000/nobel-etl-extract:latest -f Docker/Dockerfile.extract .
  ```
- **Argo Not Installing**:
  - Check the manifest URL in `apply_manifests.sh` against [Argo releases](https://github.com/argoproj/argo-workflows/releases).
- **Pods Not Running**:
  ```bash
  kubectl get pods --all-namespaces --context kind-nobel-etl-cluster
  kubectl logs <pod-name> --context kind-nobel-etl-cluster
  ```

## Cleanup

Remove the cluster and images:
```bash
kind delete cluster --name nobel-etl-cluster
docker rm -f kind-registry
docker rmi -f $(docker images -q localhost:5000/nobel-etl-*)
```

## Contributing

Feel free to submit issues or pull requests to enhance the pipeline, add tests, or improve documentation.

---

This README provides a clear guide for setting up and running your ETL pipeline, leveraging your existing scripts and structure. Let me know if you’d like to adjust any sections (e.g., add specific workflow details from `etl-workflow.yaml`)! Save it as `docs/README.md` in your project.
