#!/bin/bash

# Script to remove Nobel ETL Docker images

echo "Removing Docker images..."

docker rmi \
  localhost:5000/nobel-etl-transform \
  localhost:5000/nobel-etl-load \
  localhost:5000/nobel-etl-extract \
  localhost:5000/nobel-etl-visualize

echo "Docker images removed successfully."
