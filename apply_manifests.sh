#!/bin/bash
set -e

cd "$(dirname "$0")"

if [ ! -d "manifests" ]; then
    echo "Error: manifests/ directory not found in $(pwd)"
    exit 1
fi

CLUSTER_NAME="nobel-etl-cluster"
if ! kind get clusters | grep -q "$CLUSTER_NAME"; then
    echo "Error: Kind cluster '$CLUSTER_NAME' not found. Run build_and_upload_images.sh first."
    exit 1
fi

kubectl config use-context "kind-$CLUSTER_NAME"
echo "Switched to context kind-$CLUSTER_NAME"

echo "Installing Argo Workflows..."
kubectl create ns argo --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argo -f https://github.com/argoproj/argo-workflows/releases/download/v3.5.8/quick-start-postgres.yaml
echo "Waiting for Argo to be ready..."
kubectl wait --for=condition=available -n argo deployment/argo-server --timeout=300s || echo "Warning: argo-server not ready, proceeding anyway"
kubectl wait --for=condition=available -n argo deployment/workflow-controller --timeout=300s || echo "Warning: workflow-controller not ready, proceeding anyway"

echo "Applying Kubernetes manifests..."

echo "Applying manifests/pvc.yaml..."
kubectl apply -f manifests/pvc.yaml
sleep 5

echo "Applying manifests/mongodb.yaml..."
kubectl apply -f manifests/mongodb.yaml
sleep 30

echo "Submitting manifests/etl-workflow.yaml..."
argo submit -n default manifests/etl-workflow.yaml --watch

echo "All manifests applied and workflow completed successfully!"