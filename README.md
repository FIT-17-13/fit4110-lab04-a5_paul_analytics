# FIT4110 Lab 04 - Team Analytics Docker Packaging

This repository contains the Lab 04 submission for `team-analytics` in the Smart Campus Operations Platform case study.

Lab 04 proves that the service can be packaged, run, health-checked, and tested consistently inside a Docker container.

## Service

The service is a FastAPI analytics API that accepts mock campus events. For Lab 04, events are stored in memory. TimescaleDB or another persistent store can be added in Lab 05.

Main endpoints:

- `GET /health`
- `POST /events`
- `GET /events/latest`
- `GET /events/{event_id}`
- `GET /analytics/summary`

Auth-protected endpoints require:

```text
Authorization: Bearer local-dev-token
```

The analytics boundary used for tests is:

```text
value: 0 to 100
```

Values from `90` to `100` are accepted but return `X-Warning: high-analytics-value`.

## Required Artifacts

- `Dockerfile`
- `.dockerignore`
- `.env.example`
- `RUN_LOCAL.md`
- `contracts/team-analytics.openapi.yaml`
- `postman/collections/team-analytics.postman_collection.json`
- `postman/environments/team-analytics_local.postman_environment.json`
- `reports/newman-lab04-local.xml`
- `reports/newman-lab04-local.html`

## Quick Start

Install Newman/Prism/Spectral dependencies:

```bash
npm install
```

Build the Docker image:

```bash
docker build -t fit4110/analytics-service:lab04 .
```

Run the container:

```bash
docker run --rm \
  --name fit4110-analytics-lab04 \
  -p 8000:8000 \
  --env-file .env.example \
  fit4110/analytics-service:lab04
```

Check health:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "analytics-service",
  "version": "0.4.0"
}
```

Run Newman against the running container:

```bash
npm run test:local
```

Reports are written to:

```text
reports/newman-lab04-local.xml
reports/newman-lab04-local.html
```

## Useful Commands

```bash
make install
make lint
make mock
make test-mock
make build
make run
make test-docker
make stop
```

Suggested registry tag:

```text
ghcr.io/<owner>/team-analytics:v0.1.0-team-analytics
```
