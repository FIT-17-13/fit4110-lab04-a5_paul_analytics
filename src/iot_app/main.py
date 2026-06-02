import os
from datetime import datetime, timezone
from enum import Enum
from http import HTTPStatus
from typing import Dict, List, Optional

from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, Response, status
from http.client import responses as HTTP_STATUS_CODES
# Ensure older references to status.HTTP_STATUS_CODES work
setattr(status, "HTTP_STATUS_CODES", HTTP_STATUS_CODES)
from fastapi.exceptions import RequestValidationError
import traceback
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


SERVICE_NAME = os.getenv("SERVICE_NAME", "analytics-service")
SERVICE_VERSION = os.getenv("SERVICE_VERSION", "0.4.0")
AUTH_TOKEN = os.getenv("AUTH_TOKEN", "local-dev-token")


app = FastAPI(
    title="FIT4110 Lab 04 - Analytics Service",
    version=SERVICE_VERSION,
    description=(
        "Dockerized Smart Campus Analytics API for Lab 04. "
        "The service accepts mock campus events and exposes recent events for verification."
    ),
)


class AnalyticsEventType(str, Enum):
    occupancy = "occupancy"
    energy = "energy"
    safety = "safety"
    maintenance = "maintenance"


class AnalyticsUnit(str, Enum):
    percent = "percent"
    count = "count"
    score = "score"
    kwh = "kwh"


class RiskLevel(str, Enum):
    normal = "normal"
    watch = "watch"
    high = "high"


class ProblemDetails(BaseModel):
    type: str = "about:blank"
    title: str
    status: int = Field(..., ge=400, le=599)
    detail: str
    instance: Optional[str] = None


class HealthResponse(BaseModel):
    status: str
    service: str
    version: str


class AnalyticsEventCreate(BaseModel):
    source: str = Field(..., min_length=3, examples=["iot-ingestion"])
    event_type: AnalyticsEventType = Field(..., examples=["occupancy"])
    location_id: str = Field(..., min_length=3, examples=["B1-F2-R201"])
    value: float = Field(
        ...,
        ge=0,
        le=100,
        description="Lab 04 analytics boundary: value must be between 0 and 100.",
        examples=[76.5],
    )
    unit: AnalyticsUnit = Field(default=AnalyticsUnit.percent, examples=["percent"])
    timestamp: str = Field(..., examples=["2026-05-13T08:30:00+07:00"])


class AnalyticsEvent(BaseModel):
    event_id: str
    source: str
    event_type: AnalyticsEventType
    location_id: str
    value: float
    unit: AnalyticsUnit
    risk_level: RiskLevel
    timestamp: str
    created_at: str


class AnalyticsEventAccepted(BaseModel):
    event_id: str
    event_type: AnalyticsEventType
    accepted: bool
    risk_level: RiskLevel
    created_at: str


EVENTS: List[Dict] = []


def build_problem(
    *,
    status_code: int,
    title: str,
    detail: str,
    instance: Optional[str] = None,
    problem_type: str = "about:blank",
) -> Dict:
    problem = {
        "type": problem_type,
        "title": title,
        "status": status_code,
        "detail": detail,
    }
    if instance:
        problem["instance"] = instance
    return problem


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    try:
        if isinstance(exc.detail, dict):
            problem = exc.detail
        else:
            problem = build_problem(
                status_code=exc.status_code,
                title=HTTP_STATUS_CODES.get(exc.status_code, "HTTP Error"),
                detail=str(exc.detail),
                instance=str(request.url.path),
            )

        problem.setdefault("status", exc.status_code)
        problem.setdefault("title", HTTP_STATUS_CODES.get(exc.status_code, "HTTP Error"))
        problem.setdefault("type", "about:blank")
        problem.setdefault("detail", "Request failed")
        problem.setdefault("instance", str(request.url.path))

        return JSONResponse(
            status_code=exc.status_code,
<<<<<<< HEAD
            content=problem,
            media_type="application/problem+json",
            headers=getattr(exc, "headers", None),
        )
    except Exception:
        # If the exception handler itself fails, log traceback and return safe ProblemDetails
        tb = traceback.format_exc()
        print('Exception in http_exception_handler:', tb)
        safe = build_problem(
            status_code=500,
            title="Internal Server Error",
            detail="An internal error occurred while handling an HTTP exception",
            instance=str(request.url.path),
            problem_type="about:blank",
        )
        return JSONResponse(status_code=500, content=safe, media_type="application/problem+json")
=======
            title=HTTPStatus(exc.status_code).phrase,
            detail=str(exc.detail),
            instance=str(request.url.path),
        )

    problem.setdefault("status", exc.status_code)
    problem.setdefault("title", HTTPStatus(exc.status_code).phrase)
    problem.setdefault("type", "about:blank")
    problem.setdefault("detail", "Request failed")
    problem.setdefault("instance", str(request.url.path))

    return JSONResponse(
        status_code=exc.status_code,
        content=problem,
        media_type="application/problem+json",
        headers=getattr(exc, "headers", None),
    )
>>>>>>> d5bf33e36489a1da60e6a7f2768b75276b56ee04


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    first_error = exc.errors()[0] if exc.errors() else {}
    location = ".".join(str(item) for item in first_error.get("loc", []))
    message = first_error.get("msg", "Request validation error")
    detail = f"{location}: {message}" if location else message

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=build_problem(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            title="Validation error",
            detail=detail,
            instance=str(request.url.path),
            problem_type="https://smart-campus.local/problems/validation-error",
        ),
        media_type="application/problem+json",
    )


def verify_bearer_token(authorization: Optional[str] = Header(default=None)) -> None:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=build_problem(
                status_code=status.HTTP_401_UNAUTHORIZED,
                title="Unauthorized",
                detail="Missing Authorization header",
                problem_type="https://smart-campus.local/problems/unauthorized",
            ),
        )

    expected = f"Bearer {AUTH_TOKEN}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=build_problem(
                status_code=status.HTTP_401_UNAUTHORIZED,
                title="Unauthorized",
                detail="Invalid bearer token",
                problem_type="https://smart-campus.local/problems/unauthorized",
            ),
        )


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def next_event_id() -> str:
    today = datetime.now(timezone.utc).strftime("%Y%m%d")
    return f"A-{today}-{len(EVENTS) + 1:04d}"


def classify_risk(value: float) -> RiskLevel:
    if value >= 90:
        return RiskLevel.high
    if value >= 75:
        return RiskLevel.watch
    return RiskLevel.normal


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service=SERVICE_NAME,
        version=SERVICE_VERSION,
    )


@app.post(
    "/events",
    response_model=AnalyticsEventAccepted,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_bearer_token)],
    responses={
        401: {"model": ProblemDetails},
        422: {"model": ProblemDetails},
    },
)
def create_event(payload: AnalyticsEventCreate, response: Response) -> AnalyticsEventAccepted:
    risk_level = classify_risk(payload.value)
    if risk_level == RiskLevel.high:
        response.headers["X-Warning"] = "high-analytics-value"

    event_id = next_event_id()
    created_at = now_iso()

    item = {
        "event_id": event_id,
        "source": payload.source,
        "event_type": payload.event_type.value,
        "location_id": payload.location_id,
        "value": payload.value,
        "unit": payload.unit.value,
        "risk_level": risk_level.value,
        "timestamp": payload.timestamp,
        "created_at": created_at,
    }
    EVENTS.append(item)

    return AnalyticsEventAccepted(
        event_id=event_id,
        event_type=payload.event_type,
        accepted=True,
        risk_level=risk_level,
        created_at=created_at,
    )


@app.get("/events/latest", dependencies=[Depends(verify_bearer_token)])
def latest_events(
    location_id: Optional[str] = Query(default=None),
    limit: int = Query(default=10, ge=1, le=100),
) -> Dict[str, List[Dict]]:
    items = EVENTS

    if location_id:
        items = [item for item in items if item["location_id"] == location_id]

    return {"items": items[-limit:]}


@app.get("/events/{event_id}", dependencies=[Depends(verify_bearer_token)])
def get_event(event_id: str) -> Dict:
    for item in EVENTS:
        if item["event_id"] == event_id:
            return item

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=build_problem(
            status_code=status.HTTP_404_NOT_FOUND,
            title="Not Found",
            detail=f"Analytics event {event_id} does not exist",
            instance=f"/events/{event_id}",
            problem_type="https://smart-campus.local/problems/not-found",
        ),
    )


@app.get("/analytics/summary", dependencies=[Depends(verify_bearer_token)])
def analytics_summary(location_id: Optional[str] = Query(default=None)) -> Dict:
    items = EVENTS
    if location_id:
        items = [item for item in items if item["location_id"] == location_id]

    count = len(items)
    average_value = round(sum(item["value"] for item in items) / count, 2) if count else 0
    high_risk_count = len([item for item in items if item["risk_level"] == RiskLevel.high.value])

    return {
        "location_id": location_id,
        "event_count": count,
        "average_value": average_value,
        "high_risk_count": high_risk_count,
    }
