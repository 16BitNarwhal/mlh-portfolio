#!/bin/bash

for arg in "$@"; do
    if [ $arg="remote" ]; then
        git fetch
        git reset origin/main --hard
    fi
done

docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build
