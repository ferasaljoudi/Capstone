#!/bin/bash

IMAGE_NAME="ferasaljoudi/ifsdriveralert:latest"

if [[ "$(docker images -q $IMAGE_NAME 2> /dev/null)" != "" ]]; then
    echo "Removing old image $IMAGE_NAME..."
    docker rmi -f $IMAGE_NAME
fi

echo "Building the Docker image..."
docker-compose build

echo "Pushing the image to Docker Hub..."
docker push $IMAGE_NAME

echo "Deployment complete."
