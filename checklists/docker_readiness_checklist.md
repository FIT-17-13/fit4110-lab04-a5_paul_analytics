# Docker Readiness Checklist

## Dockerfile

- [x] Has a reasonable base image: `python:3.11-slim`.
- [x] Has `WORKDIR`.
- [x] Copies dependencies before source to use build cache.
- [x] Has `EXPOSE 8000`.
- [x] Has `CMD`.
- [x] Has `HEALTHCHECK` calling `GET /health`.
- [x] Runs as non-root user: `appuser`.
- [x] Does not contain real secrets.

## Runtime

- [x] Container runs.
- [x] Port mapping works: `8000:8000`.
- [x] `/health` returns `200`.
- [x] Startup/API logs are visible through `docker logs`.
- [x] Runtime config is supplied through `.env.example`.

## Testing

- [x] Postman collection runs against the container.
- [x] Newman reports are generated in `reports/`.
- [x] Functional tests pass.
- [x] Auth tests pass on local/container.
- [x] Negative tests pass on local/container.
- [x] Boundary tests pass: `value=100` accepted, `value=101` rejected.
- [x] Error responses use `application/problem+json` ProblemDetails shape.

## Evidence

- [x] Docker build log summary is in `reports/docker-evidence.md`.
- [x] Docker run log/status is in `reports/docker-evidence.md`.
- [x] `curl /health` result is in `reports/docker-evidence.md`.
- [x] Newman HTML/XML reports exist.
- [x] Local image tag follows lab convention.
- [ ] Registry push is pending until an owner/token is available.
