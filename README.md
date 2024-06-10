# GitHub Dashboard Microservices
# GitHub Dashboard Microservices

This project sets up a microservices architecture for a GitHub dashboard application using Docker Swarm. The services include:
- `github-service`: Fetches top-rated GitHub repositories.
- `users-service`: Manages user data and favorite repositories.
- `dashboard-service`: Frontend dashboard to view and manage repositories.
- `redis`: In-memory data structure store used by `users-service`.

## Prerequisites

- Docker
- Docker Compose
- Docker Swarm initialized on your machine

## Setup Instructions

### Step 1: Initialize Docker Swarm

If Docker Swarm is not already initialized on your machine, run:

```bash
docker swarm init
```

Compose and spin up services
```bash
docker compose -f stack.yml -p zest_app up -d
```
open the [dashboard](http://localhost:3000/)

```url
http://localhost:3000/
```