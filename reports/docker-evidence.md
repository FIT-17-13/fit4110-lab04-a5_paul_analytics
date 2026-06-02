# Docker Evidence - Lab 04

## Team

- Team name: team-analytics
- Service: analytics-service
- Image tag: fit4110/analytics-service:lab04
- Version tag: fit4110/analytics-service:v0.1.0-team-analytics
- Evidence date: 2026-06-02

## 1. Build Evidence

Command:

```bash
docker build -t fit4110/analytics-service:lab04 .
```

Result:

```text
naming to docker.io/fit4110/analytics-service:lab04 done
DONE
```

Local image tags:

```text
fit4110/analytics-service:lab04 72c7e83c9f8b 268MB
fit4110/analytics-service:v0.1.0-team-analytics 72c7e83c9f8b 268MB
```

## 2. Run Evidence

Command:

```bash
docker run -d --rm --name fit4110-analytics-lab04 -p 8000:8000 --env-file .env.example fit4110/analytics-service:lab04
```

Container status:

```text
fit4110-analytics-lab04 fit4110/analytics-service:lab04 Up 4 minutes (healthy) 0.0.0.0:8000->8000/tcp
```

Non-root user check:

```text
uid=100(appuser) gid=101(appgroup) groups=101(appgroup)
```

## 3. Healthcheck Evidence

Command:

```bash
curl http://localhost:8000/health
```

Result:

```json
{
  "status": "ok",
  "service": "analytics-service",
  "version": "0.4.0"
}
```

Docker health status:

```text
healthy
```

## 4. Newman Evidence

Command:

```bash
npm run test:local
```

Summary:

```text
requests: 13 executed, 0 failed
assertions: 22 executed, 0 failed
average response time: 13ms
```

Report paths:

```text
reports/newman-lab04-local.html
reports/newman-lab04-local.xml
```

## 5. Notes

- Current storage is in-memory for Lab 04.
- Lab 05 can add TimescaleDB or another persistent analytics store.
- Registry push is not done here because no registry owner/token was provided.
