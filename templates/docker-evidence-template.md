# Docker Evidence – Lab 04

## Team

- Team name: team-analytics
- Service: analytics-service
- Image tag: fit4110/analytics-service:lab04

## 1. Build evidence

Command:

```bash
docker build -t fit4110/analytics-service:lab04 .
```

Paste log or screenshot here.

## 2. Run evidence

Command:

```bash
docker run --rm --name fit4110-analytics-lab04 -p 8000:8000 --env-file .env.example fit4110/analytics-service:lab04
```

Paste log or screenshot here.

## 3. Healthcheck evidence

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

## 4. Newman evidence

Command:

```bash
npm run test:local
```

Report path:

```text
reports/newman-lab04-local.html
reports/newman-lab04-local.xml
```

## 5. Notes

- Known limitation:
- Next step for Lab 05:
