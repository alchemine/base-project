#!/bin/bash

# Export user id and group id
export UID=$(id -u)
export GID=$(id -g)

# Create network
docker network create inflo-network

# Create volumes
docker volume create inflo-database

# Run docker compose
docker compose -f docker/docker-compose.yml up -d --build