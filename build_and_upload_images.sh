#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -f "kind-config.yaml" ]; then
    echo "Error: kind-config.yaml not found in $(pwd)"
    exit 1
fi

if [ ! -d "Docker" ]; then
    echo "Error: Docker/ directory not found in $(pwd)"
    exit 1
fi

CLUSTER_NAME="nobel-etl-cluster"
if ! kind get clusters | grep -q "$CLUSTER_NAME"; then
    echo "Creating kind cluster '$CLUSTER_NAME'..."
    kind create cluster --name "$CLUSTER_NAME" --config kind-config.yaml
else
    echo "Kind cluster '$CLUSTER_NAME' already exists."
fi

REGISTRY_NAME="kind-registry"
REGISTRY_PORT="5000"
if ! docker ps | grep -q "$REGISTRY_NAME"; then
    echo "Starting local registry..."
    docker run -d -p "$REGISTRY_PORT:5000" --name "$REGISTRY_NAME" --network kind registry:2
    docker network connect kind "$REGISTRY_NAME" || echo "Already connected"
else
    echo "Local registry '$REGISTRY_NAME' already running."
fi

build_image() {
    local image_name="$1"
    local dockerfile="$2"
    local tag="localhost:$REGISTRY_PORT/$image_name"
    if ! docker image inspect "$tag" > /dev/null 2>&1; then
        echo "Building image: $tag"
        docker build -t "$tag" -f "$dockerfile" .
    else
        echo "Image $tag already exists, skipping build."
    fi
    echo "Pushing image: $tag"
    docker push "$tag"
}

echo "Building and pushing Docker images..."
build_image "nobel-etl-extract:latest" "Docker/Dockerfile.extract"
build_image "nobel-etl-transform:latest" "Docker/Dockerfile.transform"
build_image "nobel-etl-load:latest" "Docker/Dockerfile.load"
build_image "nobel-etl-visualize:latest" "Docker/Dockerfile.visualize"

# Load images into kind cluster
echo "Loading images into Kind cluster '$CLUSTER_NAME'..."
kind load docker-image "localhost:$REGISTRY_PORT/nobel-etl-extract:latest" --name "$CLUSTER_NAME"
kind load docker-image "localhost:$REGISTRY_PORT/nobel-etl-transform:latest" --name "$CLUSTER_NAME"
kind load docker-image "localhost:$REGISTRY_PORT/nobel-etl-load:latest" --name "$CLUSTER_NAME"
kind load docker-image "localhost:$REGISTRY_PORT/nobel-etl-visualize:latest" --name "$CLUSTER_NAME"

echo "All images have been built, pushed, and loaded successfully!"