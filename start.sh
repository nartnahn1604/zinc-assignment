#!/bin/bash

set -e

echo "Starting containers..."
docker-compose up -d

echo "Waiting for containers to become healthy..."

for service in mysql django; do
  for i in {1..30}; do
    health=$(docker inspect --format='{{.State.Health.Status}}' zinc-assignment_${service}_1 2>/dev/null || echo "notfound")
    if [ "$health" == "healthy" ]; then
      echo "$service: healthy"
      break
    elif [ "$health" == "unhealthy" ]; then
      echo "$service: unhealthy"
      exit 1
    elif [ "$health" == "notfound" ]; then
      echo "$service: container not found"
      exit 1
    fi
    sleep 2
  done
done

echo "All containers are healthy!" 