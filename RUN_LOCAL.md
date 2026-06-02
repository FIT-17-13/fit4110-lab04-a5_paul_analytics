# RUN_LOCAL.md - Run Lab 04 Team Analytics

Use these steps after cloning the repository on a clean machine.

## 1. Install test dependencies

```bash
npm install
```

## 2. Build the Docker image

```bash
docker build -t fit4110/analytics-service:lab04 .
```

## 3. Run the container

```bash
docker run --rm \
  --name fit4110-analytics-lab04 \
  -p 8000:8000 \
  --env-file .env.example \
  fit4110/analytics-service:lab04
```

## 4. Check health

Open another terminal:

```bash
curl http://localhost:8000/health
```

Expected:

```json
{
  "status": "ok",
  "service": "analytics-service",
  "version": "0.4.0"
}
```

## 5. Run Newman tests

```bash
npm run test:local
```

Reports:

```text
reports/newman-lab04-local.xml
reports/newman-lab04-local.html
```

## Optional local Python run

```bash
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn iot_app.main:app --app-dir src --host 0.0.0.0 --port 8000
```

## Stop the container

```bash
docker stop fit4110-analytics-lab04
```
